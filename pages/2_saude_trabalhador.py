import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import unicodedata

# ----------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

st.title("👷 Saúde do Trabalhador - Análise de Acidentes de Trabalho")

# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------

def normalize(text):
    """Remove acentos, espaços e deixa tudo padronizado."""
    if pd.isna(text):
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text.replace(" ", "_").upper()


def detectar_coluna_data(df):
    """Procura automaticamente a coluna que representa Data da Ocorrência."""
    possiveis = [
        "DATA_DA_OCORRENCIA",
        "DATA_OCORRENCIA",
        "DT_OCORRENCIA",
        "DATA_DA_OCORRÊNCIA",
        "DATA_ACIDENTE",
        "DATA_OCORRÊNCIA"
    ]

    cols_norm = {normalize(c): c for c in df.columns}

    for alvo in possiveis:
        if alvo in cols_norm:
            return cols_norm[alvo]

    st.error("⚠ Nenhuma coluna de data de ocorrência encontrada.")
    st.stop()


def detectar_coluna(df, nomes_possiveis):
    """Busca uma coluna entre várias possíveis, de forma automática."""
    cols_norm = {normalize(c): c for c in df.columns}
    for name in nomes_possiveis:
        if name in cols_norm:
            return cols_norm[name]
    return None


def contar_obitos(df, col_evolucao):
    """Conta óbitos pela evolução do caso."""
    if col_evolucao not in df.columns:
        return 0

    return df[col_evolucao].astype(str).str.contains(
        "OBIT|MORT|FALEC",
        case=False,
        na=False
    ).sum()


# ----------------------------------------------------------
# CARREGAR BASE REAL DO GOOGLE SHEETS
# ----------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"
    try:
        df = pd.read_csv(url, dtype=str)
    except:
        st.error("❌ Não foi possível carregar a base de dados.")
        st.stop()

    df.columns = [normalize(c) for c in df.columns]
    df.columns = [c.replace("__", "_") for c in df.columns]
    df.columns = [c.replace("_", " ") for c in df.columns]

    return df


df = carregar_dados()

# ----------------------------------------------------------
# IDENTIFICAÇÃO DE COLUNAS IMPORTANTES
# ----------------------------------------------------------

COL_DATA = detectar_coluna_data(df)

COL_SEXO = detectar_coluna(df, ["SEXO"])
COL_IDADE = detectar_coluna(df, ["IDADE", "FAIXA_ETARIA", "FAIXA ETARIA"])
COL_RACA = detectar_coluna(df, ["RACA_COR", "RAÇA_COR", "RACA", "COR"])
COL_ESCOLARIDADE = detectar_coluna(df, ["ESCOLARIDADE"])
COL_BAIRRO = detectar_coluna(df, ["BAIRRO_OCORRENCIA", "BAIRRO DE OCORRENCIA", "BAIRRO"])
COL_EVOL = detectar_coluna(df, ["EVOLUCAO", "EVOLUCAO DO CASO", "EVOLUÇÃO"])
COL_OCUPACAO = detectar_coluna(df, ["OCUPACAO", "OCUPAÇÃO"])
COL_SITUACAO_TRAB = detectar_coluna(df, ["SITUACAO_TRABALHO", "SITUACAO NO MERCADO", "SITUACAO_TRAB"])

df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")

# ----------------------------------------------------------
# CRIAÇÃO DA SEMANA EPIDEMIOLÓGICA
# ----------------------------------------------------------
df["SEMANA_EPI"] = df[COL_DATA].dt.isocalendar().week.astype(int)

# ----------------------------------------------------------
# FILTROS
# ----------------------------------------------------------

st.sidebar.header("Filtros")

df_filtrado = df.copy()

# Filtro de Semana Epidemiológica
semanas = sorted(df_filtrado["SEMANA_EPI"].dropna().unique())
semana_sel = st.sidebar.multiselect("Semana Epidemiológica", semanas)

if semana_sel:
    df_filtrado = df_filtrado[df_filtrado["SEMANA_EPI"].isin(semana_sel)]

# IDADE
if COL_IDADE:
    idades = sorted(df_filtrado[COL_IDADE].dropna().unique())
    idade_sel = st.sidebar.multiselect("Idade", idades)
    if idade_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_IDADE].isin(idade_sel)]

# SEXO
if COL_SEXO:
    sexos = sorted(df_filtrado[COL_SEXO].dropna().unique())
    sexo_sel = st.sidebar.multiselect("Sexo", sexos)
    if sexo_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_SEXO].isin(sexo_sel)]

# RAÇA/COR
if COL_RACA:
    racas = sorted(df_filtrado[COL_RACA].dropna().unique())
    raca_sel = st.sidebar.multiselect("Raça/Cor", racas)
    if raca_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_RACA].isin(raca_sel)]

# ESCOLARIDADE
if COL_ESCOLARIDADE:
    escs = sorted(df_filtrado[COL_ESCOLARIDADE].dropna().unique())
    esc_sel = st.sidebar.multiselect("Escolaridade", escs)
    if esc_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_ESCOLARIDADE].isin(esc_sel)]

# OCUPAÇÃO
if COL_OCUPACAO:
    ocup = sorted(df_filtrado[COL_OCUPACAO].dropna().unique())
    ocup_sel = st.sidebar.multiselect("Ocupação", ocup)
    if ocup_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_OCUPACAO].isin(ocup_sel)]

# SITUAÇÃO NO MERCADO DE TRABALHO
if COL_SITUACAO_TRAB:
    sit = sorted(df_filtrado[COL_SITUACAO_TRAB].dropna().unique())
    sit_sel = st.sidebar.multiselect("Situação no Mercado de Trabalho", sit)
    if sit_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_SITUACAO_TRAB].isin(sit_sel)]

# BAIRRO DE OCORRÊNCIA
if COL_BAIRRO:
    bairros = sorted(df_filtrado[COL_BAIRRO].dropna().unique())
    bairro_sel = st.sidebar.multiselect("Bairro de Ocorrência", bairros)
    if bairro_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_BAIRRO].isin(bairro_sel)]

# EVOLUÇÃO DO CASO
if COL_EVOL:
    evols = sorted(df_filtrado[COL_EVOL].dropna().unique())
    evol_sel = st.sidebar.multiselect("Evolução do Caso", evols)
    if evol_sel:
        df_filtrado = df_filtrado[df_filtrado[COL_EVOL].isin(evol_sel)]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ----------------------------------------------------------
# INDICADORES PRINCIPAIS
# ----------------------------------------------------------

st.header("📊 Indicadores Principais")

total = len(df_filtrado)
obitos = contar_obitos(df_filtrado, COL_EVOL)

# Ocupação mais afetada
if COL_OCUPACAO:
    try:
        top_ocup = df_filtrado[COL_OCUPACAO].value_counts().idxmax()
    except:
        top_ocup = "Indefinido"
else:
    top_ocup = "Indefinido"

col1, col2, col3 = st.columns(3)

col1.metric("Total de Acidentes", total)
col2.metric("Óbitos", obitos)
col3.metric("Ocupação mais afetada", top_ocup)

# ----------------------------------------------------------
# GRÁFICOS
# ----------------------------------------------------------

st.header("📈 Distribuições de Atributos")

# Idade
if COL_IDADE:
    fig = px.histogram(df_filtrado, x=COL_IDADE, title="Distribuição por Idade")
    st.plotly_chart(fig, use_container_width=True)

# Sexo
if COL_SEXO:
    df_sexo = df_filtrado[COL_SEXO].value_counts().reset_index()
    df_sexo.columns = ["SEXO", "QTD"]
    fig = px.bar(df_sexo, x="SEXO", y="QTD", title="Distribuição por Sexo")
    st.plotly_chart(fig, use_container_width=True)

# Raça/Cor
if COL_RACA:
    df_raca = df_filtrado[COL_RACA].value_counts().reset_index()
    df_raca.columns = ["RACA_COR", "QTD"]
    fig = px.bar(df_raca, x="RACA_COR", y="QTD", title="Distribuição por Raça/Cor")
    st.plotly_chart(fig, use_container_width=True)

# Escolaridade
if COL_ESCOLARIDADE:
    df_esc = df_filtrado[COL_ESCOLARIDADE].value_counts().reset_index()
    df_esc.columns = ["ESCOLARIDADE", "QTD"]
    fig = px.bar(df_esc, x="ESCOLARIDADE", y="QTD", title="Distribuição por Escolaridade")
    st.plotly_chart(fig, use_container_width=True)

# Bairro
if COL_BAIRRO:
    df_bairro = df_filtrado[COL_BAIRRO].value_counts().reset_index()
    df_bairro.columns = ["BAIRRO", "QTD"]
    fig = px.bar(df_bairro.head(20), x="BAIRRO", y="QTD", title="Top 20 Bairros com Mais Acidentes")
    st.plotly_chart(fig, use_container_width=True)

# Evolução
if COL_EVOL:
    df_ev = df_filtrado[COL_EVOL].value_counts().reset_index()
    df_ev.columns = ["EVOLUCAO", "QTD"]
    fig = px.bar(df_ev, x="EVOLUCAO", y="QTD", title="Evolução dos Casos")
    st.plotly_chart(fig, use_container_width=True)
# ----------------------------------------------------------
# TABELA FINAL
# ----------------------------------------------------------

st.header("📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

st.caption("Desenvolvido por Maviael Barros.")
st.markdown("---")
st.caption("Painel de Dengue • Versão 1.0")
