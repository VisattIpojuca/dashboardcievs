import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------
st.set_page_config(
    page_title="Oropouche - Dashboard",
    page_icon="🦟",
    layout="wide"
)

st.title("👶 Dashboard de Oropouche - Vigilância em Saúde")
st.markdown("Monitoramento de gestantes por localidade, classificação e período.")

# -------------------------------------------
# FUNÇÃO PARA CARREGAR GOOGLE SHEETS
# -------------------------------------------
@st.cache_data
def carregar_planilha(url):
    url_csv = url.replace("/edit?usp=sharing", "/export?format=csv")
    df = pd.read_csv(url_csv, dtype=str)
    return df

# Carrega a planilha
url = "https://docs.google.com/spreadsheets/d/1pk_X_h-tfpA53te1ViXcrY40SqSSI6WA/edit?usp=sharing"
df = carregar_planilha(url)

# -------------------------------------------
# NORMALIZAÇÃO DE COLUNAS
# -------------------------------------------
def normalize(text):
    if not isinstance(text, str):
        return ""
    return (
        text.strip()
        .upper()
        .replace("Á", "A")
        .replace("À", "A")
        .replace("Ã", "A")
        .replace("Â", "A")
        .replace("É", "E")
        .replace("Ê", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Õ", "O")
        .replace("Ô", "O")
        .replace("Ú", "U")
        .replace("Ç", "C")
        .replace(" ", "_")
        .replace(".", "")
        .replace("-", "_")
    )

df.columns = [normalize(col) for col in df.columns]

# -------------------------------------------
# REMOVER COLUNAS COM DADOS PESSOAIS
# -------------------------------------------
colunas_sensiveis = [
    "NOME", "PACIENTE", "MAE", "MÃE", "NOME_DA_MAE",
    "ENDERECO", "RUA", "TELEFONE", "CELULAR"
]

df = df[[col for col in df.columns if all(s not in col for s in colunas_sensiveis)]]

# -------------------------------------------
# IDENTIFICAR COLUNAS PRINCIPAIS
# -------------------------------------------

def encontrar_coluna(possiveis):
    for p in possiveis:
        p_norm = normalize(p)
        for col in df.columns:
            if normalize(col) == p_norm:
                return col
    return None

COL_LOCALIDADE = encontrar_coluna(["LOCALIDADE", "BAIRRO", "AREA"])
COL_CLASSIFICACAO = encontrar_coluna(["CLASSIFICACAO", "STATUS", "TIPO"])
COL_DATA = encontrar_coluna(["DATA", "DATA_DO_CASO", "NOTIFICACAO", "DATA_ENTRADA"])
COL_GESTANTE = encontrar_coluna(["GESTANTE", "GRAVIDEZ", "GESTACAO"])

# -------------------------------------------
# TRATAR COLUNA DE DATA
# -------------------------------------------
if COL_DATA:
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")
    df["MES"] = df[COL_DATA].dt.to_period("M").astype(str)
else:
    df["MES"] = "SEM DATA"

# -------------------------------------------
# FILTROS
# -------------------------------------------

st.sidebar.subheader("Filtros")

localidades = sorted(df[COL_LOCALIDADE].dropna().unique()) if COL_LOCALIDADE else []
classificacoes = sorted(df[COL_CLASSIFICACAO].dropna().unique()) if COL_CLASSIFICACAO else []

f_localidade = st.sidebar.multiselect("Localidade", localidades)
f_classificacao = st.sidebar.multiselect("Classificação", classificacoes)

df_filtrado = df.copy()

if f_localidade:
    df_filtrado = df_filtrado[df_filtrado[COL_LOCALIDADE].isin(f_localidade)]

if f_classificacao:
    df_filtrado = df_filtrado[df_filtrado[COL_CLASSIFICACAO].isin(f_classificacao)]

# -------------------------------------------
# INDICADORES PRINCIPAIS
# -------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Registros", len(df_filtrado))

with col2:
    if COL_GESTANTE:
        total_gestantes = df_filtrado[COL_GESTANTE].str.contains("SIM", case=False, na=False).sum()
        st.metric("Gestantes Identificadas", total_gestantes)
    else:
        st.metric("Gestantes Identificadas", "-")

with col3:
    st.metric("Períodos Registrados", df_filtrado["MES"].nunique())

# -------------------------------------------
# GRÁFICOS
# -------------------------------------------

st.subheader("📈 Distribuição por Mês")

fig_mes = px.bar(
    df_filtrado["MES"].value_counts().sort_index(),
    labels={"value": "Quantidade", "index": "Mês"},
    title="Casos por Mês"
)
st.plotly_chart(fig_mes, use_container_width=True)

# Distribuição de gestantes
if COL_GESTANTE:
    st.subheader("🤰 Distribuição de Gestantes")

    fig_gest = px.pie(
        df_filtrado,
        names=COL_GESTANTE,
        title="Proporção de Gestantes"
    )
    st.plotly_chart(fig_gest, use_container_width=True)

# Classificação por mês
if COL_CLASSIFICACAO:
    st.subheader("📊 Classificação por Mês")

    fig_class_mes = px.histogram(
        df_filtrado,
        x="MES",
        color=COL_CLASSIFICACAO,
        barmode="group",
        title="Classificação por Mês"
    )
    st.plotly_chart(fig_class_mes, use_container_width=True)

# Localidade x Classificação
if COL_LOCALIDADE and COL_CLASSIFICACAO:
    st.subheader("📍 Classificação e Localidade")

    fig_lc = px.histogram(
        df_filtrado,
        x=COL_LOCALIDADE,
        color=COL_CLASSIFICACAO,
        barmode="group",
        title="Distribuição por Localidade"
    )
    st.plotly_chart(fig_lc, use_container_width=True)

# -------------------------------------------
# TABELA FINAL
# -------------------------------------------

st.subheader("📋 Dados Filtrados")

st.dataframe(df_filtrado, use_container_width=True)
