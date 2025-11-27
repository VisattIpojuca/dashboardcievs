import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import unicodedata
from datetime import datetime

# ----------------------------------------------------------
# CONFIG DA PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

# ----------------------------------------------------------
# CSS — IDENTIDADE VISUAL INSTITUCIONAL FIXA
# ----------------------------------------------------------
st.markdown("""
<style>

:root {
    --azul-principal: #004A8D;
    --azul-secundario: #0073CF;
    --verde-ipojuca: #009D4A;
    --amarelo-ipojuca: #FFC20E;
    --cinza-claro: #F2F2F2;
    --branco: #FFFFFF;
}

/* Texto sempre preto, mesmo no modo escuro */
html, body, * {
    color: #000 !important;
}

/* Títulos amarelos */
h1, h2, h3, h4 {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 800 !important;
}

/* Parágrafos justificados */
p, li {
    text-align: justify !important;
}

/* Fundo geral fixo */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--azul-principal) !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] a {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 600;
}

/* Cards / Métricas */
.stMetric {
    background-color: var(--amarelo-ipojuca) !important;
    padding: 18px;
    border-radius: 10px;
    border-left: 6px solid var(--azul-secundario);
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}

/* Botões */
button, .stButton button {
    color: #000 !important;
    background-color: var(--cinza-claro) !important;
}

/* Fundo branco obrigatório nos gráficos Plotly */
.js-plotly-plot .plotly .main-svg {
    background-color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# TÍTULO
# ----------------------------------------------------------
st.title("👷 Saúde do Trabalhador – Análise de Acidentes de Trabalho")

# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.replace(" ", "_").upper()


def detectar_coluna(df, termos):
    cols_norm = {normalize(c): c for c in df.columns}
    for alvo in termos:
        for col_norm, original in cols_norm.items():
            if alvo in col_norm:
                return original
    return None


def contar_obitos(df, coluna):
    if coluna not in df.columns:
        return 0
    
    padroes = [
        "ÓBITO", "OBITO", "MORTE", "FALEC",
        "ÓBITO POR ACIDENTE DE TRABALHO GRAVE",
        "OBITO POR ACIDENTE DE TRABALHO GRAVE"
    ]

    serie = df[coluna].astype(str).str.upper()
    resultados = pd.DataFrame({
        p: serie.str.contains(p, case=False, na=False)
        for p in padroes
    })
    return resultados.any(axis=1).sum()

# ----------------------------------------------------------
# CARREGAR DADOS DO GOOGLE SHEETS
# ----------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"
    df = pd.read_csv(url, dtype=str)
    
    df.columns = [normalize(c) for c in df.columns]
    df.columns = [c.replace("__", "_") for c in df.columns]
    df.columns = [c.replace("_", " ") for c in df.columns]
    
    return df

df = carregar_dados()

# ----------------------------------------------------------
# IDENTIFICAÇÃO DE COLUNAS
# ----------------------------------------------------------
COL_DATA = detectar_coluna(df, ["DATA", "OCORR"])
df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")

COL_SEXO = detectar_coluna(df, ["SEXO"])
COL_IDADE = detectar_coluna(df, ["IDADE"])
COL_RACA = detectar_coluna(df, ["RACA", "RAÇA", "COR"])
COL_ESCOLARIDADE = detectar_coluna(df, ["ESCOLAR"])
COL_BAIRRO = detectar_coluna(df, ["BAIRRO"])
COL_OCUPACAO = detectar_coluna(df, ["OCUP"])
COL_SITUACAO = detectar_coluna(df, ["SITUACAO", "MERCADO"])
COL_EVOL = detectar_coluna(df, ["EVOL", "CASO", "DESFECHO"])
COL_SEMANA = detectar_coluna(df, ["SEMANA", "EPID", "SE"])

# ----------------------------------------------------------
# FILTROS
# ----------------------------------------------------------
st.sidebar.header("🔎 Filtros")
df_filtrado = df.copy()

# Período
min_d, max_d = df_filtrado[COL_DATA].min(), df_filtrado[COL_DATA].max()
data_ini, data_fim = st.sidebar.date_input(
    "Período",
    value=[min_d, max_d],
    min_value=min_d,
    max_value=max_d
)

df_filtrado = df_filtrado[
    (df_filtrado[COL_DATA] >= pd.to_datetime(data_ini)) &
    (df_filtrado[COL_DATA] <= pd.to_datetime(data_fim))
]

# Semana Epidemiológica
if COL_SEMANA:
    semanas = df[COL_SEMANA].dropna().astype(str)
    semanas = semanas.str.extract(r"(\d+)")[0].astype(int)
    semanas = sorted(semanas.unique())

    semanas_sel = st.sidebar.multiselect("Semana Epidemiológica", semanas)

    if semanas_sel:
        semanas_df = df_filtrado[COL_SEMANA].astype(str).str.extract(r"(\d+)")[0].astype(float)
        df_filtrado = df_filtrado[semanas_df.isin(semanas_sel)]

# Filtros gerais
def add_filtro(label, coluna):
    global df_filtrado
    if coluna:
        opcoes = sorted(df[coluna].dropna().unique())
        escolhidos = st.sidebar.multiselect(label, opcoes)
        if escolhidos:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(escolhidos)]

add_filtro("Sexo", COL_SEXO)
add_filtro("Idade", COL_IDADE)
add_filtro("Raça/Cor", COL_RACA)
add_filtro("Escolaridade", COL_ESCOLARIDADE)
add_filtro("Ocupação", COL_OCUPACAO)
add_filtro("Situação no Mercado de Trabalho", COL_SITUACAO)
add_filtro("Bairro", COL_BAIRRO)
add_filtro("Evolução", COL_EVOL)

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

# ----------------------------------------------------------
# INDICADORES
# ----------------------------------------------------------
st.header("📊 Indicadores Principais")

total = len(df_filtrado)
obitos = contar_obitos(df_filtrado, COL_EVOL)

top_ocup = df_filtrado[COL_OCUPACAO].value_counts().idxmax() if COL_OCUPACAO else "Indefinido"

c1, c2, c3 = st.columns(3)
c1.metric("Total de Acidentes", total)
c2.metric("Óbitos", obitos)
c3.metric("Ocupação mais afetada", top_ocup)

# ----------------------------------------------------------
# GRÁFICOS — sempre com fundo branco
# ----------------------------------------------------------

# Cores institucionais
cores = ["#004A8D", "#009D4A", "#FFC20E", "#0073CF"]

st.header("📈 Distribuições")

# Sexo
if COL_SEXO:
    ds = df_filtrado[COL_SEXO].value_counts().reset_index()
    ds.columns = ["SEXO", "QTD"]
    fig = px.pie(ds, names="SEXO", values="QTD",
                 title="Distribuição por Sexo",
                 hole=0.3)
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Raça/cor x sexo
if COL_RACA and COL_SEXO:
    d = df_filtrado[[COL_RACA, COL_SEXO]].dropna()
    d = d.groupby([COL_RACA, COL_SEXO]).size().reset_index(name="QTD")
    fig = px.bar(d, x=COL_RACA, y="QTD", color=COL_SEXO,
                 title="Raça/Cor por Sexo",
                 color_discrete_sequence=cores)
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Idade
if COL_IDADE:
    fig = px.histogram(df_filtrado, x=COL_IDADE, title="Distribuição por Idade",
                       color_discrete_sequence=[cores[0]])
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Escolaridade
if COL_ESCOLARIDADE:
    df_esc = df_filtrado[COL_ESCOLARIDADE].value_counts().reset_index()
    df_esc.columns = ["ESCOLARIDADE", "QTD"]
    fig = px.bar(df_esc, x="ESCOLARIDADE", y="QTD",
                 title="Escolaridade",
                 color_discrete_sequence=[cores[3]])
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Bairro
if COL_BAIRRO:
    df_bairro = df_filtrado[COL_BAIRRO].value_counts().reset_index()
    df_bairro.columns = ["BAIRRO", "QTD"]
    fig = px.bar(df_bairro.head(20), x="BAIRRO", y="QTD",
                 title="Top 20 Bairros",
                 color_discrete_sequence=[cores[1]])
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Evolução
if COL_EVOL:
    df_ev = df_filtrado[COL_EVOL].value_counts().reset_index()
    df_ev.columns = ["EVOLUCAO", "QTD"]
    fig = px.bar(df_ev, x="EVOLUCAO", y="QTD",
                 title="Evolução dos Casos",
                 color_discrete_sequence=[cores[2]])
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# TABELA
# ----------------------------------------------------------
st.header("📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

st.markdown("---")

st.caption("Painel de Saúde do Trabalhador • Versão 1.0")
st.caption("Desenvolvido por Maviael Barros.")
