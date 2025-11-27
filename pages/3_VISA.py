# 3_visa.py
# Painel VISA Ipojuca — Versão revisada e estilizada
# Requisitos: streamlit, pandas, plotly, openpyxl

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import plotly.express as px

# --------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------------
st.set_page_config(
    page_title="Painel VISA Ipojuca",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Painel de Produção – Vigilância Sanitária de Ipojuca")

# --------------------------------------------------------
# CONSTANTES / PALETA INSTITUCIONAL
# --------------------------------------------------------
GOOGLE_SHEETS_URL = (
    "https://docs.google.com/spreadsheets/d/1zsM8Zxdc-MnXSvV_OvOXiPoc1U4j-FOn/edit?usp=sharing"
)

USERS = {
    "default": {"role": "standard"},
}

NOME_MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",
    4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro",
    10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

CORES = {
    "azul": "#004A8D",
    "azul_sec": "#0073CF",
    "verde": "#009D4A",
    "amarelo": "#FFC20E",
    "cinza_claro": "#F2F2F2",
    "branco": "#FFFFFF",
}

# --------------------------------------------------------
# CSS — MESMO TEMA DOS OUTROS PAINÉIS
# --------------------------------------------------------
def aplicar_css():
    st.markdown(f"""
    <style>
    :root {{
        --azul-principal: {CORES["azul"]};
        --azul-secundario: {CORES["azul_sec"]};
        --verde-ipojuca: {CORES["verde"]};
        --amarelo-ipojuca: {CORES["amarelo"]};
        --cinza-claro: {CORES["cinza_claro"]};
        --branco: {CORES["branco"]};
    }}

    /* Texto principal da área central */
    [data-testid="stAppViewContainer"] body,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] .stMarkdown {{
        color: #0073CF !important;
    }}

    /* Títulos amarelos na área principal */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 800 !important;
    }}

    /* Parágrafos justificados */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li {{
        text-align: justify !important;
    }}

    /* Fundo geral */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--azul-principal) !important;
    }}
    [data-testid="stSidebar"] a {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 600;
    }}

    /* Título "Filtros" na sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 800 !important;
    }}

    /* RÓTULOS DOS FILTROS (Período, Ano, Mês, etc.) – AZUL CLARO */
    [data-testid="stSidebar"] div[class*="stMarkdown"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stTextInput label {{
        color: {CORES["azul_sec"]} !important;
        font-weight: 600 !important;
    }}

    /* TEXTO E CAMPOS DOS FILTROS – tema claro (padrão azul escuro) */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stMultiSelect * {{
        color: {CORES["azul"]} !important;
    }}

    /* Campo de período (DateInput) com texto azul claro no modo claro */
    [data-testid="stSidebar"] .stDateInput input {{
        color: {CORES["azul_sec"]} !important;
    }}

    /* Campos de texto, número, select e multiselect: fundo branco */
    [data-testid="stSidebar"] .stTextInput > div > div,
    [data-testid="stSidebar"] .stNumberInput > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {{
        background-color: var(--branco) !important;
        border-radius: 6px !important;
    }}

    /* DateInput (Período) – fundo branco */
    [data-testid="stSidebar"] .stDateInput > div > div {{
        background-color: var(--branco) !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {{
        color: #2f6bbd !important;
    }}

    /* OPÇÕES SELECIONADAS (chips) */
    [data-testid="stSidebar"] .stMultiSelect div[aria-selected="true"],
    [data-testid="stSidebar"] .stSelectbox div[aria-selected="true"] {{
        background-color: {CORES["verde"]} !important;
        color: white !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"],
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] * {{
        background-color: {CORES["verde"]} !important;
        color: white !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stTextInput > div,
    [data-testid="stSidebar"] .stNumberInput > div,
    [data-testid="stSidebar"] .stDateInput > div {{
        border-color: var(--azul-secundario) !important;
        border-radius: 6px !important;
    }}

    /* POPUP DO CALENDÁRIO (DateInput) – base: texto claro e fundo escuro */
    [data-testid="stSidebar"] .stDateInput [data-baseweb="datepicker"],
    [data-testid="stSidebar"] .stDateInput [data-baseweb="calendar"] {{
        background-color: #222831 !important;
    }}

    [data-testid="stSidebar"] .stDateInput [data-baseweb="datepicker"] *,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="calendar"] * {{
        color: #FFFFFF !important;
    }}

    /* Dias e cabeçalhos de dia da semana */
    [data-testid="stSidebar"] .stDateInput [data-baseweb="calendar"] td,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="calendar"] th {{
        color: #FFFFFF !important;
    }}

    /* Cabeçalho do calendário: mês, ano e setas em azul claro */
    [data-testid="stSidebar"] .stDateInput [data-baseweb="datepicker"] select,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="datepicker"] [role="button"] {{
        color: {CORES["azul_sec"]} !important;
    }}

    /* Fundo dos selects de mês/ano */
    [data-testid="stSidebar"] .stDateInput [data-baseweb="datepicker"] select {{
        background-color: #393E46 !important;
    }}

    /* Dia selecionado em destaque */
    [data-testid="stSidebar"] .stDateInput [aria-selected="true"] {{
        background-color: {CORES["azul_sec"]} !important;
        color: #FFFFFF !important;
    }}

    /* GRÁFICOS – se usar Plotly, garantir fundo branco (opcional aqui) */
    .js-plotly-plot .plotly .bg,
    .js-plotly-plot .plotly .plotly-background,
    .js-plotly-plot .plotly .paper,
    .js-plotly-plot .plotly .plotbg {{
        fill: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }}
    .js-plotly-plot text {{
        fill: {CORES["azul"]} !important;
        color: {CORES["azul"]} !important;
    }}
    .element-container .js-plotly-plot {{
        border: 1px solid #000000 !important;
        border-radius: 4px !important;
        padding: 4px !important;
        background-color: #FFFFFF !important;
    }}

    /* MENU PÁGINAS NA SIDEBAR (caso tenha multipage) */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button[aria-current="page"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }}

    /* ===========================
       MODO ESCURO
       =========================== */
    @media (prefers-color-scheme: dark) {{

        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] .stMultiSelect,
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stNumberInput,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stDateInput,
        [data-testid="stSidebar"] .stTextInput,
        [data-testid="stSidebar"] .stMultiSelect * {{
            color: #FFFFFF !important;
        }}

        /* Rótulos dos filtros continuam azul claro */
        [data-testid="stSidebar"] div[class*="stMarkdown"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stNumberInput label,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stDateInput label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stTextInput label {{
            color: {CORES["azul_sec"]} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSidebar"] .stDateInput input {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"],
        [data-testid="stSidebar"] ul[role="listbox"] {{
            background-color: {CORES["azul_sec"]} !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"] *,
        [data-testid="stSidebar"] ul[role="listbox"] * {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="option"],
        [data-testid="stSidebar"] li[role="option"] {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="option"][aria-selected="true"],
        [data-testid="stSidebar"] li[role="option"][aria-selected="true"] {{
            background-color: rgba(0,0,0,0.2) !important;
            color: #FFFFFF !important;
        }}
    }}

    /* Métricas */
    .stMetric {{
        background-color: var(--amarelo-ipojuca) !important;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid var(--azul-secundario);
        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
    }}

    /* Botões */
    button, .stButton button {{
        color: #FFFFFF !important;
        background-color: var(--cinza-claro) !important;
        border-radius: 6px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

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

    # Ano / mês de entrada
    if "ENTRADA" in df.columns:
        df["ANO_ENTRADA"] = df["ENTRADA"].dt.year
        df["MES_ENTRADA"] = df["ENTRADA"].dt.month

        # Semana Epidemiológica (derivada de ENTRADA)
        try:
            df["SE_SEMANA"] = df["ENTRADA"].dt.isocalendar().week.astype("Int64").astype(str)
        except Exception:
            df["SE_SEMANA"] = df["ENTRADA"].dt.week.astype("Int64").astype(str)
    else:
        df["ANO_ENTRADA"] = pd.NA
        df["MES_ENTRADA"] = pd.NA
        df["SE_SEMANA"] = pd.NA

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
            except Exception:
                d.to_excel(writer, sheet_name=sheet[:28] + "_", index=False)
    return out.getvalue()


# --------------------------------------------------------
# FILTROS (incluindo Semana Epidemiológica)
# --------------------------------------------------------
def aplicar_filtros(df: pd.DataFrame) -> pd.DataFrame:
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
            format_func=lambda m: NOME_MESES.get(m, str(m)),
        )
    else:
        # Garante que ENTRADA é datetime
        if "ENTRADA" not in df.columns or df["ENTRADA"].isna().all():
            st.error("Não há dados de data de entrada para filtrar por intervalo.")
            st.stop()

        min_data = df["ENTRADA"].min().date()
        max_data = df["ENTRADA"].max().date()

        inicio = st.sidebar.date_input("Início", min_data, min_value=min_data, max_value=max_data)
        fim = st.sidebar.date_input("Fim", max_data, min_value=min_data, max_value=max_data)

    # Classificação (risco)
    riscos = sorted(df["CLASSIFICAÇÃO"].dropna().unique()) if "CLASSIFICAÇÃO" in df.columns else []
    sel_risco = st.sidebar.multiselect("Classificação (Risco)", riscos, default=riscos)

    # Semana Epidemiológica (usando SE_SEMANA)
    if "SE_SEMANA" in df.columns:
        semanas = sorted(df["SE_SEMANA"].dropna().unique())
    else:
        semanas = []
    sel_se = st.sidebar.multiselect("Semana Epidemiológica", semanas, default=semanas)

    filtro_df = df.copy()

    # Filtro por período
    if modo == "Ano/Mês":
        filtro_df = filtro_df[
            (filtro_df["ANO_ENTRADA"] == ano) &
            (filtro_df["MES_ENTRADA"].isin(mes_sel))
        ]
    else:
        filtro_df = filtro_df[
            (filtro_df["ENTRADA"].dt.date >= inicio) &
            (filtro_df["ENTRADA"].dt.date <= fim)
        ]

    # Filtro por classificação (risco)
    if sel_risco and "CLASSIFICAÇÃO" in filtro_df.columns:
        filtro_df = filtro_df[filtro_df["CLASSIFICAÇÃO"].isin(sel_risco)]

    # Filtro de Semana Epidemiológica
    if sel_se and "SE_SEMANA" in filtro_df.columns:
        filtro_df = filtro_df[filtro_df["SE_SEMANA"].isin(sel_se)]

    if filtro_df.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        st.stop()

    return filtro_df


# --------------------------------------------------------
# INDICADORES E TABELA
# --------------------------------------------------------
def calcular_indicadores(filtro_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # DEADLINES
    filtro_df["DEADLINE_30"] = filtro_df["ENTRADA"] + timedelta(days=30)
    filtro_df["DEADLINE_90"] = filtro_df["ENTRADA"] + timedelta(days=90)

    filtro_df["REALIZOU_30"] = (
        filtro_df["1ª INSPEÇÃO"].notna() & (filtro_df["1ª INSPEÇÃO"] <= filtro_df["DEADLINE_30"])
    )

    filtro_df["FINALIZOU_90"] = (
        filtro_df["DATA CONCLUSÃO"].notna() & (filtro_df["DATA CONCLUSÃO"] <= filtro_df["DEADLINE_90"])
    )

    # Tabela resumida
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

    tabela["Mês"] = tabela["MES_ENTRADA"].apply(lambda m: NOME_MESES.get(m, str(m)))
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

    # KPIs
    total = len(filtro_df)
    realizou = int(filtro_df["REALIZOU_30"].sum())
    finalizou = int(filtro_df["FINALIZOU_90"].sum())

    p30 = round(realizou / total * 100, 2) if total else 0
    p90 = round(finalizou / total * 100, 2) if total else 0

    kpis = {
        "total": total,
        "realizou": realizou,
        "finalizou": finalizou,
        "p30": p30,
        "p90": p90,
    }

    return tabela, kpis


def mostrar_tabela_e_kpis(tabela: pd.DataFrame, kpis: dict):
    st.subheader("📊 Indicadores Mensais")
    st.dataframe(tabela, use_container_width=True)

    st.subheader("📈 Dados do Período")
    c1, c2, c3 = st.columns(3)
    c1.metric("Entradas (período)", kpis["total"])
    c2.metric("% Inspeções ≤ 30 dias", f"{kpis['p30']}%")
    c3.metric("% Conclusões ≤ 90 dias", f"{kpis['p90']}%")


# --------------------------------------------------------
# DOWNLOAD
# --------------------------------------------------------
def mostrar_download(filtro_df: pd.DataFrame, tabela: pd.DataFrame):
    try:
        excel_bytes = gerar_excel_bytes({"dados_filtrados": filtro_df, "tabela": tabela})
        st.download_button(
            "📥 Baixar Excel",
            data=excel_bytes,
            file_name="relatorio_visa.xlsx",
        )
    except Exception:
        st.info("📁 O download do Excel não está disponível neste ambiente.")


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
def main():
    aplicar_css()

    # Usuário padrão (simples)
    st.session_state["user"] = "default"
    st.session_state["role"] = "standard"

    # Carrega dados
    df = carregar_planilha_google(GOOGLE_SHEETS_URL)
    if df.empty:
        st.error("Nenhum dado encontrado.")
        st.stop()

    # Detecção de colunas (se no futuro quiser usar coord/território)
    col_coord = detectar_coluna(df, ["COORDENAÇÃO", "COORDENACAO", "COORDENADORIA", "COORD"])
    col_territorio = detectar_coluna(df, ["TERRITÓRIO", "TERRITORIO", "TERRITORY", "TERR"])

    # Aplica filtros (inclui Semana Epidemiológica corrigida)
    filtro_df = aplicar_filtros(df)

    # Indicadores / Tabela
    tabela, kpis = calcular_indicadores(filtro_df)
    mostrar_tabela_e_kpis(tabela, kpis)

    # Download
    mostrar_download(filtro_df, tabela)

    st.caption("Painel VISA Ipojuca – Acesso público")
    st.markdown("---")
    st.caption("Painel de Indicadores da Vigilância Sanitária • Versão 1.0 (tema institucional)")
    st.caption("Desenvolvido por Maviael Barros.")


if __name__ == "__main__":
    main()
