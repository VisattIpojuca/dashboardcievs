import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import unicodedata
from datetime import datetime, timedelta

# ------------------------------------------------------------
# CONFIGURAÇÃO DO PAINEL
# ------------------------------------------------------------
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

st.title("👷 Saúde do Trabalhador – Painel Analítico")


# ------------------------------------------------------------
# FUNÇÃO UNIVERSAL PARA NORMALIZAR COLUNAS
# ------------------------------------------------------------
def normalizar(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.strip()
    texto = texto.replace(" ", "")
    texto = texto.replace("_", "")
    texto = texto.upper()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join([c for c in texto if not unicodedata.combining(c)])
    return texto


# ------------------------------------------------------------
# FUNÇÃO PARA DETECTAR COLUNA POR PALAVRAS-CHAVE
# ------------------------------------------------------------
def detectar_coluna(df, lista_chaves):
    colunas_norm = {normalizar(c): c for c in df.columns}

    for col_norm, col_original in colunas_norm.items():
        for chave in lista_chaves:
            if chave in col_norm:
                return col_original
    return None


# ------------------------------------------------------------
# CARREGAR PLANILHA – GOOGLE SHEETS
# ------------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"
    df = pd.read_csv(url, dtype=str)

    for col in df.columns:
        df[col] = df[col].replace("", np.nan)

    return df


df = carregar_dados()

if df is None or df.empty:
    st.error("❌ Não foi possível carregar a base de dados.")
    st.stop()


# ------------------------------------------------------------
# DETECÇÃO DE TODAS AS COLUNAS IMPORTANTES
# ------------------------------------------------------------
COL_DATA      = detectar_coluna(df, ["DATAOCORRENCIA", "DATADEOCORRENCIA", "OCORRENCIA"])
COL_SEXO      = detectar_coluna(df, ["SEXO"])
COL_IDADE     = detectar_coluna(df, ["IDADE"])
COL_RACA      = detectar_coluna(df, ["RACA", "COR", "RACACOR"])
COL_ESCOL     = detectar_coluna(df, ["ESCOLARIDADE"])
COL_OCUP      = detectar_coluna(df, ["OCUPACAO"])
COL_SIT_MERC  = detectar_coluna(df, ["SITUACAO", "MERCADO"])
COL_BAIRRO    = detectar_coluna(df, ["BAIRRO"])
COL_EVOL      = detectar_coluna(df, ["EVOLUCAO", "EVOL", "DESFECHO"])
COL_OBITO     = detectar_coluna(df, ["OBITO", "MORTE", "FALEC", "ÓBITO"])


# ------------------------------------------------------------
# CONVERTER DATA
# ------------------------------------------------------------
if COL_DATA:
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce", dayfirst=True)
    df["SEMANA"] = df[COL_DATA].dt.isocalendar().week
else:
    st.error("⚠ Não foi possível identificar a coluna de DATA DA OCORRÊNCIA.")
    st.stop()


# ------------------------------------------------------------
# SIDEBAR – FILTROS
# ------------------------------------------------------------
st.sidebar.header("Filtros")

def filtro(col, label):
    if col and col in df.columns:
        return st.sidebar.multiselect(
            label,
            options=sorted(df[col].dropna().unique().tolist()),
            default=None
        )
    return None


filtro_sexo   = filtro(COL_SEXO, "Sexo")
filtro_idade  = filtro(COL_IDADE, "Idade")
filtro_raca   = filtro(COL_RACA, "Raça/Cor")
filtro_escol  = filtro(COL_ESCOL, "Escolaridade")
filtro_ocup   = filtro(COL_OCUP, "Ocupação")
filtro_sit    = filtro(COL_SIT_MERC, "Situação no Mercado de Trabalho")
filtro_bairro = filtro(COL_BAIRRO, "Bairro de Ocorrência")
filtro_evol   = filtro(COL_EVOL, "Evolução do Caso")

f_semana = st.sidebar.multiselect(
    "Semana Epidemiológica",
    options=sorted(df["SEMANA"].dropna().unique().tolist())
)


# ------------------------------------------------------------
# APLICAR FILTROS
# ------------------------------------------------------------
df_filtrado = df.copy()

def aplicar(df, coluna, valores):
    if coluna and coluna in df.columns and valores:
        return df[df[coluna].isin(valores)]
    return df

df_filtrado = aplicar(df_filtrado, COL_SEXO, filtro_sexo)
df_filtrado = aplicar(df_filtrado, COL_IDADE, filtro_idade)
df_filtrado = aplicar(df_filtrado, COL_RACA, filtro_raca)
df_filtrado = aplicar(df_filtrado, COL_ESCOL, filtro_escol)
df_filtrado = aplicar(df_filtrado, COL_OCUP, filtro_ocup)
df_filtrado = aplicar(df_filtrado, COL_SIT_MERC, filtro_sit)
df_filtrado = aplicar(df_filtrado, COL_BAIRRO, filtro_bairro)
df_filtrado = aplicar(df_filtrado, COL_EVOL, filtro_evol)

if f_semana:
    df_filtrado = df_filtrado[df_filtrado["SEMANA"].isin(f_semana)]


# ------------------------------------------------------------
# INDICADORES PRINCIPAIS  (AGORA COM ÓBITOS)
# ------------------------------------------------------------
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total = len(df_filtrado)

# Média semanal
media_semanal = df_filtrado.groupby("SEMANA").size().mean() if total > 0 else 0

# Ocupação mais afetada
ocupacao_top = (
    df_filtrado[COL_OCUP].mode().iloc[0]
    if COL_OCUP and df_filtrado[COL_OCUP].notna().any()
    else "Não informado"
)

# Número de óbitos
def contar_obitos(df):
    if COL_OBITO and COL_OBITO in df.columns:
        # conta qualquer variação contendo indicativos de óbito
        return df[COL_OBITO].str.contains("OBIT|MORT|FALEC", case=False, na=False).sum()
    elif COL_EVOL and COL_EVOL in df.columns:
        return df[COL_EVOL].str.contains("OBIT|MORT|FALEC", case=False, na=False).sum()
    return 0

total_obitos = contar_obitos(df_filtrado)

with col1:
    st.metric("Total de Ocorrências", total)

with col2:
    st.metric("Média Semanal", f"{media_semanal:.1f}")

with col3:
    st.metric("Ocupação mais afetada", ocupacao_top)

with col4:
    st.metric("Óbitos Registrados", total_obitos)


# ------------------------------------------------------------
# GRÁFICO TEMPORAL POR SEMANA
# ------------------------------------------------------------
st.header("📈 Ocorrências por Semana Epidemiológica")

df_sem = df_filtrado.groupby("SEMANA").size().reset_index()
df_sem.columns = ["Semana", "Ocorrências"]

fig_tempo = px.line(
    df_sem,
    x="Semana",
    y="Ocorrências",
    markers=True,
    title="Série Temporal por Semana Epidemiológica"
)

st.plotly_chart(fig_tempo, use_container_width=True)


# ------------------------------------------------------------
# FUNÇÃO PARA GRÁFICOS DE BARRAS
# ------------------------------------------------------------
def grafico_barras(col, titulo):
    if col and col in df_filtrado.columns:
        df_plot = df_filtrado[col].value_counts().reset_index()
        df_plot.columns = [col, "Quantidade"]
        fig = px.bar(df_plot, x=col, y="Quantidade", title=titulo)
        st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# GRÁFICOS DEMOGRÁFICOS
# ------------------------------------------------------------
st.header("📊 Distribuições")

grafico_barras(COL_IDADE, "Distribuição por Idade")
grafico_barras(COL_SEXO, "Distribuição por Sexo")
grafico_barras(COL_RACA, "Distribuição por Raça/Cor")
grafico_barras(COL_ESCOL, "Distribuição por Escolaridade")
grafico_barras(COL_BAIRRO, "Distribuição por Bairro de Ocorrência")
grafico_barras(COL_EVOL, "Distribuição por Evolução do Caso")


# ------------------------------------------------------------
# TABELA DETALHADA
# ------------------------------------------------------------
st.header("📋 Tabela Detalhada")

st.dataframe(df_filtrado, use_container_width=True)


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.markdown("*Painel de Saúde do Trabalhador – Versão 1.0*")
