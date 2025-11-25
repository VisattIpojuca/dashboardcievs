import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import unicodedata
from datetime import datetime

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


def detectar_coluna_similar(df, termos_busca):
    """
    Busca uma coluna compatível por similaridade.
    Ex: EVOLUÇÃO DO CASO → EVOLUCAO_DO_CASO → casa com 'EVOLU', 'CASO'.
    """
    colunas_norm = {normalize(c): c for c in df.columns}

    for col_norm, col_original in colunas_norm.items():
        for termo in termos_busca:
            if termo in col_norm:
                return col_original

    return None


def contar_obitos(df, coluna):
    """Conta óbitos pela coluna de evolução detectando várias formas de escrita."""
    if coluna not in df.columns:
        return 0

    padrao = r"(OBIT|MORT|FALEC)"
    return df[coluna].astype(str).str.contains(padrao, case=False, na=False).sum()


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

    # Normalizar nomes das colunas
    df.columns = [normalize(c) for c in df.columns]
    df.columns = [c.replace("__", "_") for c in df.columns]
    df.columns = [c.replace("_", " ") for c in df.columns]

    return df


df = carregar_dados()

# ----------------------------------------------------------
# DETECÇÃO AUTOMÁTICA DE COLUNAS
# ----------------------------------------------------------

# Coluna de data
COL_DATA = detectar_coluna_similar(df, ["DATA", "OCORR"])

# Converter data
df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")

# Demais colunas
COL_SEXO = detectar_coluna_similar(df, ["SEXO"])
COL_IDADE = detectar_coluna_similar(df, ["IDADE"])
COL_RACA = detectar_coluna_similar(df, ["RACA", "COR"])
COL_ESCOLARIDADE = detectar_coluna_similar(df, ["ESCOLAR"])
COL_BAIRRO = detectar_coluna_similar(df, ["BAIRRO"])
COL_OCUPACAO = detectar_coluna_similar(df, ["OCUP"])
COL_SITUACAO_TRAB = detectar_coluna_similar(df, ["SITUACAO", "MERCADO"])
COL_EVOL = detectar_coluna_similar(df, ["EVOL", "CASO", "DESFECHO"])

# ----------------------------------------------------------
# FILTROS
# ----------------------------------------------------------

st.sidebar.header("Filtros")

df_filtrado = df.copy()

# Intervalo de datas
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

# Função para filtros
def add_filtro(nome, coluna):
    global df_filtrado
    if coluna and coluna in df_filtrado.columns:
        valores = sorted(df_filtrado[coluna].dropna().unique())
        selecionados = st.sidebar.multiselect(nome, valores)
        if selecionados:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(selecionados)]


add_filtro("Sexo", COL_SEXO)
add_filtro("Idade", COL_IDADE)
add_filtro("Raça/Cor", COL_RACA)
add_filtro("Escolaridade", COL_ESCOLARIDADE)
add_filtro("Ocupação", COL_OCUPACAO)
add_filtro("Situação no Mercado de Trabalho", COL_SITUACAO_TRAB)
add_filtro("Bairro de Ocorrência", COL_BAIRRO)
add_filtro("Evolução do Caso", COL_EVOL)

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
    top_ocup = df_filtrado[COL_OCUPACAO].value_counts().idxmax()
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
    df_sx = df_filtrado[COL_SEXO].value_counts().reset_index()
    df_sx.columns = ["SEXO", "QTD"]
    fig = px.bar(df_sx, x="SEXO", y="QTD", title="Distribuição por Sexo")
    st.plotly_chart(fig, use_container_width=True)

# Raça/Cor
if COL_RACA:
    df_rc = df_filtrado[COL_RACA].value_counts().reset_index()
    df_rc.columns = ["RACA_COR", "QTD"]
    fig = px.bar(df_rc, x="RACA_COR", y="QTD", title="Distribuição por Raça/Cor")
    st.plotly_chart(fig, use_container_width=True)

# Escolaridade
if COL_ESCOLARIDADE:
    df_es = df_filtrado[COL_ESCOLARIDADE].value_counts().reset_index()
    df_es.columns = ["ESCOLARIDADE", "QTD"]
    fig = px.bar(df_es, x="ESCOLARIDADE", y="QTD", title="Escolaridade")
    st.plotly_chart(fig, use_container_width=True)

# Bairro
if COL_BAIRRO:
    df_b = df_filtrado[COL_BAIRRO].value_counts().reset_index()
    df_b.columns = ["BAIRRO", "QTD"]
    fig = px.bar(df_b.head(20), x="BAIRRO", y="QTD", title="Top 20 Bairros")
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
