# pages/1_oropouche.py
"""
Dashboard Oropouche — Página Streamlit (tema institucional)
- Usa Data da Notificação para séries mensais
- Filtros: Localidade, Classificação, Semana Epidemiológica, Sexo, Raça/Cor
- Tabela final oculta: MES, DATA_DE_NASCIMENTO, NOME, RUA, TELEFONE, etc.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# CONFIG / TEMA DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Oropouche - Dashboard",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# PALETA / CORES INSTITUCIONAIS
# ---------------------------------------------------------
CORES = {
    "azul": "#004A8D",
    "azul_sec": "#0073CF",
    "verde": "#009D4A",
    "amarelo": "#FFC20E",
    "cinza_claro": "#F2F2F2",
    "branco": "#FFFFFF",
}

PALETA = [
    CORES["azul"],
    CORES["verde"],
    CORES["amarelo"],
    CORES["azul_sec"],
]

# ---------------------------------------------------------
# CSS – TEMA INSTITUCIONAL + AJUSTES NOS FILTROS
# ---------------------------------------------------------
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

    /* Texto principal em preto (sem usar * para não quebrar componentes internos) */
    body, p, li, span, label, .stMarkdown {{
        color: #000 !important;
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
    p, li {{
        text-align: justify !important;
        color: #000 !important;
    }}

    /* Fundo geral */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--azul-principal) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    [data-testid="stSidebar"] a {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 600;
    }}

    /* ------------------------------
       WIDGETS DE FILTRO NA SIDEBAR
       ------------------------------ */

    /* Texto dos inputs/selects sempre azul */
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

    /* ESTILO PADRÃO DAS TAGS (opções exibidas, não selecionadas): fundo branco, texto azul */
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {CORES["branco"]} !important;
        color: {CORES["azul"]} !important;
        border-radius: 12px !important;
        border: 1px solid {CORES["azul_sec"]} !important;
    }}

    /* TAGS / OPÇÕES SELECIONADAS: fundo verde, texto branco */
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"][aria-selected="true"],
    [data-testid="stSidebar"] .stMultiSelect div[aria-selected="true"],
    [data-testid="stSidebar"] .stSelectbox div[aria-selected="true"] {{
        background-color: {CORES["verde"]} !important;
        color: white !important;
        border-color: {CORES["verde"]} !important;
    }}

    /* Borda dos campos de filtro em azul */
    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stTextInput > div,
    [data-testid="stSidebar"] .stNumberInput > div,
    [data-testid="stSidebar"] .stDateInput > div {{
        border-color: {CORES["azul_sec"]} !important;
    }}

    /* (Removido o @media prefers-color-scheme: dark para manter igual em claro/escuro) */

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
        color: #000 !important;
        background-color: {CORES["cinza_claro"]} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Fonte de dados (local primeiro, senão Google)
# ---------------------------------------------------------
LOCAL_DATA_PATH = "/mnt/data/PLANILHA REDESIM 2025 (Integrador).xlsx"
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1pk_X_h-tfpA53te1ViXcrY40SqSSI6WA/export?format=csv"


@st.cache_data(ttl=600)
def carregar_dados(local_path: str | None = None,
                   gsheet_csv_url: str | None = None) -> pd.DataFrame:
    df = pd.DataFrame()

    # 1) tenta arquivo local
    if local_path:
        try:
            if os.path.exists(local_path):
                try:
                    df = pd.read_excel(local_path, dtype=str)
                except Exception:
                    df = pd.read_csv(local_path, dtype=str)
                return df
        except Exception:
            pass

    # 2) tenta Google Sheet CSV
    if gsheet_csv_url:
        try:
            df = pd.read_csv(gsheet_csv_url, dtype=str)
            return df
        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


# ---------------------------------------------------------
# Normalização de nomes de coluna e detectores
# ---------------------------------------------------------
def normalize(col_name: str) -> str:
    if not isinstance(col_name, str):
        return ""
    s = col_name.strip().upper()
    replacements = {
        "Á": "A", "À": "A", "Ã": "A", "Â": "A",
        "É": "E", "Ê": "E",
        "Í": "I",
        "Ó": "O", "Õ": "O", "Ô": "O",
        "Ú": "U",
        "Ç": "C"
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.replace(" ", "_").replace(".", "").replace("-", "_").replace("/", "_")
    return s


def detectar(df: pd.DataFrame, candidatos: list[str]) -> str | None:
    candidatos_norm = [normalize(x) for x in candidatos]
    for cand in candidatos_norm:
        if cand in df.columns:
            return cand
    return None


# ---------------------------------------------------------
# Remoção de dados sensíveis
# ---------------------------------------------------------
def remover_sensiveis(df: pd.DataFrame,
                      col_localidade: str | None,
                      col_data: str | None) -> pd.DataFrame:
    sensiveis_tokens = [
        "NOME", "PACIENTE", "MAE", "MAE_", "RUA", "ENDERECO", "ENDEREÇO",
        "TELEFONE", "CELULAR", "CPF",
        "DATA_DE_NASCIMENTO", "NASCIMENTO", "DN", "DATA_NASC"
    ]
    cols_para_remover = [c for c in df.columns if any(tok in c for tok in sensiveis_tokens)]
    cols_para_remover = [
        c for c in cols_para_remover
        if c not in {col_localidade, col_data}
    ]
    df_limpo = df.drop(columns=cols_para_remover, errors="ignore")
    return df_limpo


# ---------------------------------------------------------
# Filtros (sidebar)
# ---------------------------------------------------------
def opcoes(df: pd.DataFrame, col: str | None):
    if col and col in df.columns:
        return sorted(df[col].dropna().unique().tolist())
    return []


def aplicar_filtros(df: pd.DataFrame,
                    col_localidade: str | None,
                    col_classificacao: str | None,
                    col_sexo: str | None,
                    col_raca: str | None) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    localidades = opcoes(df, col_localidade)
    classificacoes = opcoes(df, col_classificacao)
    sexos = opcoes(df, col_sexo)
    racas = opcoes(df, col_raca)
    semanas = opcoes(df, "SE_SEMANA")

    f_localidade = st.sidebar.multiselect("Localidade", options=localidades, default=localidades)
    f_classificacao = st.sidebar.multiselect("Classificação", options=classificacoes, default=classificacoes)
    f_sexo = st.sidebar.multiselect("Sexo", options=sexos, default=sexos)
    f_raca = st.sidebar.multiselect("Raça/Cor", options=racas, default=racas)
    f_semana = st.sidebar.multiselect("Semana Epidemiológica", options=semanas, default=semanas)

    df_filtrado = df.copy()
    if f_localidade and col_localidade in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado[col_localidade].isin(f_localidade)]
    if f_classificacao and col_classificacao in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado[col_classificacao].isin(f_classificacao)]
    if f_sexo and col_sexo in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado[col_sexo].isin(f_sexo)]
    if f_raca and col_raca in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado[col_raca].isin(f_raca)]
    if f_semana and "SE_SEMANA" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["SE_SEMANA"].isin(f_semana)]

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
    return df_filtrado


# ---------------------------------------------------------
# Criação de colunas de data/semana
# ---------------------------------------------------------
def tratar_data(df: pd.DataFrame,
                col_data: str | None,
                col_semana_epid: str | None) -> pd.DataFrame:
    # Data (Data da Notificação)
    if col_data and col_data in df.columns:
        df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors="coerce")
        if df[col_data].notna().any():
            df["MES_NOTIF"] = df[col_data].dt.to_period("M").astype(str)
        else:
            st.warning("Coluna de Data encontrada, mas todos os valores são inválidos. Usando SEM_DATA.")
            df["MES_NOTIF"] = "SEM_DATA"
    else:
        df["MES_NOTIF"] = "SEM_DATA"

    # Semana epidemiológica:
    # 1) se existir coluna própria (SEMANA_EPIDEMIOLOGICA etc.), usa ela
    if col_semana_epid and col_semana_epid in df.columns:
        df["SE_SEMANA"] = (
            df[col_semana_epid]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)  # pega só o número
            .fillna("IGNORADO")
        )
    # 2) senão, deriva da data (se tiver)
    elif col_data and col_data in df.columns and df[col_data].notna().any():
        try:
            df["SE_SEMANA"] = df[col_data].dt.isocalendar().week.astype("Int64").astype(str)
        except Exception:
            df["SE_SEMANA"] = df[col_data].dt.week.astype(str)
    else:
        df["SE_SEMANA"] = "SEM_SEMANA"

    return df


# ---------------------------------------------------------
# Indicadores
# ---------------------------------------------------------
def mostrar_indicadores(df_filtrado: pd.DataFrame, col_gestante: str | None):
    st.header("📊 Indicadores Rápidos")
    c1, c2 = st.columns(2)
    c1.metric("Registros (filtrados)", len(df_filtrado))

    if col_gestante and col_gestante in df_filtrado.columns:
        gestantes = df_filtrado[col_gestante].astype(str).str.contains("SIM", case=False, na=False).sum()
        c2.metric("Gestantes identificadas", gestantes)
    else:
        c2.metric("Gestantes identificadas", "—")


# ---------------------------------------------------------
# Gráficos
# ---------------------------------------------------------
def mostrar_graficos(df_filtrado: pd.DataFrame,
                     col_localidade: str | None,
                     col_classificacao: str | None,
                     col_sexo: str | None,
                     col_raca: str | None):
    st.markdown("## 📈 Séries Temporais")

    # 1) Casos por mês
    st.subheader("Casos por Mês")
    if "MES_NOTIF" in df_filtrado.columns:
        series = (
            df_filtrado
            .groupby("MES_NOTIF")
            .size()
            .reset_index(name="CASOS")
            .sort_values("MES_NOTIF")
        )
        fig_mes = px.line(
            series,
            x="MES_NOTIF",
            y="CASOS",
            markers=True,
            title="Evolução mensal dos casos",
            labels={"MES_NOTIF": "Mês (YYYY-MM)", "CASOS": "Casos"},
            color_discrete_sequence=[CORES["azul"]]
        )
        fig_mes.update_layout(xaxis=dict(tickangle=-45))
        st.plotly_chart(fig_mes, use_container_width=True)

    # 2) Classificação por mês
    st.subheader("Classificação por Mês")
    if "MES_NOTIF" in df_filtrado.columns and col_classificacao in df_filtrado.columns:
        class_mes = (
            df_filtrado
            .groupby(["MES_NOTIF", col_classificacao])
            .size()
            .reset_index(name="CASOS")
            .sort_values("MES_NOTIF")
        )
        fig_class = px.line(
            class_mes,
            x="MES_NOTIF",
            y="CASOS",
            color=col_classificacao,
            markers=True,
            title="Classificação por Mês",
            labels={"MES_NOTIF": "Mês (YYYY-MM)", "CASOS": "Casos"},
            color_discrete_sequence=PALETA
        )
        fig_class.update_layout(xaxis=dict(tickangle=-45))
        st.plotly_chart(fig_class, use_container_width=True)

    # 3) Localidade x Classificação
    if col_localidade and col_classificacao and col_localidade in df_filtrado.columns:
        st.subheader("Distribuição por Localidade")
        loc_summary = (
            df_filtrado
            .groupby([col_localidade, col_classificacao])
            .size()
            .reset_index(name="CASOS")
            .sort_values("CASOS", ascending=False)
        )
        fig_loc = px.bar(
            loc_summary,
            x=col_localidade,
            y="CASOS",
            color=col_classificacao,
            barmode="group",
            title="Localidade x Classificação",
            color_discrete_sequence=PALETA
        )
        st.plotly_chart(fig_loc, use_container_width=True)

    # 4) Sexo (pizza)
    if col_sexo and col_sexo in df_filtrado.columns:
        st.subheader("Distribuição por Sexo")
        sex_summary = df_filtrado[col_sexo].value_counts().reset_index()
        sex_summary.columns = [col_sexo, "QTD"]
        fig_sex = px.pie(
            sex_summary,
            names=col_sexo,
            values="QTD",
            title="Sexo",
            color_discrete_sequence=PALETA
        )
        st.plotly_chart(fig_sex, use_container_width=True)

    # 5) Raça/Cor x Sexo
    if col_raca and col_sexo and col_raca in df_filtrado.columns and col_sexo in df_filtrado.columns:
        st.subheader("Raça/Cor por Sexo")
        cruz = df_filtrado.groupby([col_raca, col_sexo]).size().reset_index(name="QTD")
        fig_raca_sexo = px.bar(
            cruz,
            x=col_raca,
            y="QTD",
            color=col_sexo,
            barmode="group",
            title="Raça/Cor por Sexo",
            color_discrete_sequence=PALETA
        )
        st.plotly_chart(fig_raca_sexo, use_container_width=True)


# ---------------------------------------------------------
# Tabela final
# ---------------------------------------------------------
def mostrar_tabela(df_filtrado: pd.DataFrame):
    st.markdown("## 📋 Dados Filtrados")

    ocultar = ["MES_NOTIF", "SE_SEMANA"]
    df_exib = df_filtrado.drop(columns=[c for c in ocultar if c in df_filtrado.columns],
                               errors="ignore")

    df_exib = df_exib[
        [
            c for c in df_exib.columns
            if "NASC" not in c.upper() and "DATA_DE_NASC" not in c.upper()
        ]
    ]

    st.dataframe(df_exib.reset_index(drop=True), use_container_width=True)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    aplicar_css()

    st.title("🦟 Dashboard de Oropouche - Vigilância em Saúde")
    st.markdown(
        "Monitoramento por localidade, classificação e período. "
        "Dados sensíveis ocultos automaticamente."
    )

    df_raw = carregar_dados(local_path=LOCAL_DATA_PATH, gsheet_csv_url=GSHEET_URL)
    if df_raw is None or df_raw.empty:
        st.error("Dados não encontrados (arquivo local ausente e/ou planilha online inacessível).")
        st.stop()

    # Normalizar nomes
    orig_cols = list(df_raw.columns)
    df = df_raw.rename(columns={orig: normalize(orig) for orig in orig_cols})

    # Detectar colunas importantes
    col_localidade = detectar(df, ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO", "TERRITÓRIO"])
    col_classificacao = detectar(df, ["CLASSIFICACAO", "CLASSIFICAÇÃO", "STATUS", "TIPO", "CLASS"])
    col_sexo = detectar(df, ["SEXO", "GENERO", "GÊNERO"])
    col_raca = detectar(df, ["RACA_COR", "RAÇA_COR", "RACA", "COR", "RACA/COR"])
    col_gestante = detectar(df, ["GESTANTE", "GRAVIDEZ", "GESTACAO"])
    # inclui "Data da Notificação"
    col_data = detectar(df, [
        "DATA DA NOTIFICAÇÃO", "DATA DA NOTIFICACAO",
        "DATA_DA_NOTIFICAÇÃO", "DATA_DA_NOTIFICACAO",
        "DATA_NOTIFICACAO", "DATA_DE_NOTIFICACAO",
        "DATA NOTIFICAÇÃO", "DATA DE NOTIFICACAO",
        "DATA_DE_NOTIFICAÇÃO",
        "NOTIFICACAO", "DATA_DO_CASO", "DATA_ENTRADA", "DATA", "DATA_NOTIF", "DATE"
    ])
    col_semana_epid = detectar(df, [
        "SEMANA_EPIDEMIOLOGICA", "SEMANA EPIDEMIOLOGICA",
        "SEMANA_EPIDEMIOLÓGICA", "SEMANA EPIDEMIOLÓGICA",
        "SEMANA", "SEMANA_EP", "SE"
    ])

    # Sexo: F/M -> Feminino/Masculino
    if col_sexo and col_sexo in df.columns:
        df[col_sexo] = (
            df[col_sexo]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace({
                "F": "Feminino",
                "M": "Masculino"
            })
        )

    # Tratar data + semana epidemiológica
    df = tratar_data(df, col_data, col_semana_epid)

    # Remover sensíveis
    df = remover_sensiveis(df, col_localidade, col_data)

    # Filtros
    df_filtrado = aplicar_filtros(df, col_localidade, col_classificacao, col_sexo, col_raca)

    # Indicadores
    mostrar_indicadores(df_filtrado, col_gestante)

    # Gráficos
    mostrar_graficos(df_filtrado, col_localidade, col_classificacao, col_sexo, col_raca)

    # Tabela
    mostrar_tabela(df_filtrado)

    st.markdown("---")
    st.caption("Painel de Oropouche • Versão 1.0 (tema institucional)")
    st.caption("Desenvolvido por Maviael Barros.")


if __name__ == "__main__":
    main()
