# 3_visa.py
# Painel VISA Ipojuca — Versão revisada e corrigida
# Requisitos: streamlit, pandas, plotly, openpyxl

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import plotly.express as px

# --------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------------
st.set_page_config(page_title="Painel VISA Ipojuca", layout="wide")
st.title("📊 Painel de Produção – Vigilância Sanitária de Ipojuca")

# --------------------------------------------------------
# CONSTANTES
# --------------------------------------------------------
GOOGLE_SHEETS_URL = (
    "https://docs.google.com/spreadsheets/d/1zsM8Zxdc-MnXSvV_OvOXiPoc1U4j-FOn/edit?usp=sharing"
)

# Usuário padrão (visualização simples)
USERS = {
    "default": {"role": "standard"},
}

NOME_MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",
    4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro",
    10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------

def converter_para_csv(url: str) -> str | None:
    """Converte URL de Google Sheets para CSV."""
    if not isinstance(url, str):
        return None
    partes = url.split("/d/")
    if len(partes) < 2:
        return None
    sheet_id = partes[1].split("/")[0]
    if not sheet_id:
        return None
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"


@st.cache_data(ttl=600)
def carregar_planilha_google(url_original: str) -> pd.DataFrame:
    """Carrega planilha Google Sheets em CSV e normaliza colunas."""
    url_csv = converter_para_csv(url_original)
    if not url_csv:
        st.error("URL do Google Sheets inválida.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(url_csv)
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return pd.DataFrame()

    df.columns = [str(c).strip() for c in df.columns]

    # Datas
    for col in ["ENTRADA", "1ª INSPEÇÃO", "DATA CONCLUSÃO"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    if "ENTRADA" in df.columns:
        df["ANO_ENTRADA"] = df["ENTRADA"].dt.year
        df["MES_ENTRADA"] = df["ENTRADA"].dt.month
    else:
        df["ANO_ENTRADA"] = pd.NA
        df["MES_ENTRADA"] = pd.NA

    if "SITUAÇÃO" in df.columns:
        df["SITUAÇÃO"] = df["SITUAÇÃO"].fillna("").astype(str).str.upper()

    if "CLASSIFICAÇÃO" in df.columns:
        df["CLASSIFICAÇÃO"] = df["CLASSIFICAÇÃO"].fillna("").astype(str).str.title()

    return df


def detectar_coluna(df, candidatos):
    for c in candidatos:
        if c in df.columns:
            return c
    return None


def gerar_excel_bytes(dfs: dict):
    """Gera um arquivo Excel usando openpyxl (compatível com Streamlit Cloud)."""
    out = BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        for name, d in dfs.items():
            sheet = str(name)[:31] if name else "Sheet"
            try:
                d.to_excel(writer, sheet_name=sheet, index=False)
            except:
                d.to_excel(writer, sheet_name=sheet[:28] + "_", index=False)
    return out.getvalue()

# --------------------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------------------

df = carregar_planilha_google(GOOGLE_SHEETS_URL)
if df.empty:
    st.error("Nenhum dado encontrado.")
    st.stop()

col_coord = detectar_coluna(df, ["COORDENAÇÃO", "COORDENACAO", "COORDENADORIA", "COORD"])
col_territorio = detectar_coluna(df, ["TERRITÓRIO", "TERRITORIO", "TERRITORY", "TERR"])

# --------------------------------------------------------
# USUÁRIO PADRÃO AUTOMÁTICO
# --------------------------------------------------------

st.session_state["user"] = "default"
st.session_state["role"] = "standard"

# --------------------------------------------------------
# FILTROS
# --------------------------------------------------------

st.sidebar.header("Filtros")

modo = st.sidebar.radio("Período:", ["Ano/Mês", "Intervalo de datas"])

anos = sorted(df["ANO_ENTRADA"].dropna().unique()) if "ANO_ENTRADA" in df.columns else []
ANO_ATUAL = datetime.now().year
if not anos:
    anos = [ANO_ATUAL]

ano_sel = ANO_ATUAL if ANO_ATUAL in anos else anos[0]

if modo == "Ano/Mês":
    ano = st.sidebar.selectbox("Ano", anos, index=anos.index(ano_sel))
    meses = sorted(df[df["ANO_ENTRADA"] == ano]["MES_ENTRADA"].dropna().unique())
    mes_sel = st.sidebar.multiselect(
        "Mês",
        options=meses,
        default=meses,
        format_func=lambda m: NOME_MESES[m],
    )
else:
    inicio = st.sidebar.date_input("Início", df["ENTRADA"].min().date())
    fim = st.sidebar.date_input("Fim", df["ENTRADA"].max().date())

# Classificação (risco)
riscos = sorted(df["CLASSIFICAÇÃO"].dropna().unique()) if "CLASSIFICAÇÃO" in df.columns else []
sel_risco = st.sidebar.multiselect("Classificação (Risco)", riscos, default=riscos)

# Usuário padrão NÃO vê filtros avançados
sel_ter = []
sel_coord = []

# --------------------------------------------------------
# APLICA FILTROS
# --------------------------------------------------------

filtro_df = df.copy()

if modo == "Ano/Mês":
    filtro_df = filtro_df[(filtro_df["ANO_ENTRADA"] == ano) & (filtro_df["MES_ENTRADA"].isin(mes_sel))]
else:
    filtro_df = filtro_df[(filtro_df["ENTRADA"].dt.date >= inicio) & (filtro_df["ENTRADA"].dt.date <= fim)]

if sel_risco:
    filtro_df = filtro_df[filtro_df["CLASSIFICÁÇÃO".replace("Á", "A")] .isin(sel_risco)]

# --------------------------------------------------------
# CÁLCULO DE INDICADORES
# --------------------------------------------------------

filtro_df["DEADLINE_30"] = filtro_df["ENTRADA"] + timedelta(days=30)
filtro_df["DEADLINE_90"] = filtro_df["ENTRADA"] + timedelta(days=90)

filtro_df["REALIZOU_30"] = (
    filtro_df["1ª INSPEÇÃO"].notna() & (filtro_df["1ª INSPEÇÃO"] <= filtro_df["DEADLINE_30"])
)

filtro_df["FINALIZOU_90"] = (
    filtro_df["DATA CONCLUSÃO"].notna() & (filtro_df["DATA CONCLUSÃO"] <= filtro_df["DEADLINE_90"])
)

# --------------------------------------------------------
# TABELA RESUMIDA
# --------------------------------------------------------

tabela = (
    filtro_df.groupby(["ANO_ENTRADA", "MES_ENTRADA"])
    .agg(
        Entradas=("ENTRADA", "count"),
        Realizou30=("REALIZOU_30", "sum"),
        Perc30=("REALIZOU_30", lambda x: round((x.sum() / len(x)) * 100, 2)),
        Finalizou90=("FINALIZOU_90", "sum"),
        Perc90=("FINALIZOU_90", lambda x: round((x.sum() / len(x)) * 100, 2)),
    )
    .reset_index()
)

tabela["Mês"] = tabela["MES_ENTRADA"].apply(lambda m: NOME_MESES[m])
tabela = tabela.sort_values(["ANO_ENTRADA", "MES_ENTRADA"], ascending=[False, True])

tabela = tabela[
    ["ANO_ENTRADA", "Mês", "Entradas", "Realizou30", "Perc30", "Finalizou90", "Perc90"]
]

tabela.columns = [
    "Ano",
    "Mês",
    "Entradas",
    "Realizou a inspeção em até 30 dias",
    "% Realizou 30 dias",
    "Finalizou o processo em até 90 dias",
    "% Finalizou 90 dias",
]

st.subheader("📊 Indicadores Mensais")
st.dataframe(tabela, use_container_width=True)

# --------------------------------------------------------
# KPIs
# --------------------------------------------------------

total = len(filtro_df)
realizou = int(filtro_df["REALIZOU_30"].sum())
finalizou = int(filtro_df["FINALIZOU_90"].sum())

p30 = round(realizou / total * 100, 2) if total else 0
p90 = round(finalizou / total * 100, 2) if total else 0

c1, c2, c3 = st.columns(3)
c1.metric("Entradas (período)", total)
c2.metric("% Inspeções ≤30 dias", f"{p30}%")
c3.metric("% Conclusões ≤90 dias", f"{p90}%")

# --------------------------------------------------------
# DOWNLOAD SEGURO (SEM ERRO NA TELA)
# --------------------------------------------------------

try:
    excel_bytes = gerar_excel_bytes({"dados_filtrados": filtro_df, "tabela": tabela})

    st.download_button(
        "📥 Baixar Excel",
        data=excel_bytes,
        file_name="relatorio_visa.xlsx",
    )

except Exception:
    st.info("📁 O download do Excel não está disponível neste ambiente.")

st.caption("Painel VISA Ipojuca – Acesso público")

st.markdown("---")

st.caption("Painel de Indicadores da Vigilância Sanitária • Versão 1.0")
st.caption("Desenvolvido por Maviael Barros.")
