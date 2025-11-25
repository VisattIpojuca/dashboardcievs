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

st.title("🦟 Dashboard de Oropouche - Vigilância em Saúde")
st.markdown("Monitoramento por localidade, classificação e período, com proteção de dados sensíveis.")

# -------------------------------------------
# FUNÇÃO PARA CARREGAR GOOGLE SHEETS
# -------------------------------------------
@st.cache_data
def carregar_planilha(url):
    url_csv = url.replace("/edit?usp=sharing", "/export?format=csv")
    df = pd.read_csv(url_csv, dtype=str)
    return df

url = "https://docs.google.com/spreadsheets/d/1pk_X_h-tfpA53te1ViXcrY40SqSSI6WA/edit?usp=sharing"
df = carregar_planilha(url)

# -------------------------------------------
# NORMALIZAÇÃO
# -------------------------------------------
def normalize(text):
    if not isinstance(text, str):
        return ""
    return (
        text.strip().upper()
        .replace("Á","A").replace("À","A").replace("Ã","A").replace("Â","A")
        .replace("É","E").replace("Ê","E")
        .replace("Í","I")
        .replace("Ó","O").replace("Õ","O").replace("Ô","O")
        .replace("Ú","U")
        .replace("Ç","C")
        .replace(" ", "_").replace(".", "").replace("-", "_")
    )

df.columns = [normalize(col) for col in df.columns]

# -------------------------------------------
# REMOVER COLUNAS SENSÍVEIS
# -------------------------------------------
colunas_sensiveis = [
    "NOME", "PACIENTE", "MAE", "MÃE", "NOME_DA_MAE",
    "ENDERECO", "RUA", "TELEFONE", "CELULAR",
    "DATA_DE_NASCIMENTO", "NASCIMENTO", "DN"
]
df = df[[c for c in df.columns if all(s not in c for s in colunas_sensiveis)]]

# -------------------------------------------
# IDENTIFICANDO COLUNAS IMPORTANTES
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
COL_SEXO = encontrar_coluna(["SEXO", "GENERO"])
COL_RACA = encontrar_coluna(["RACA_COR", "RAÇA/COR", "COR", "RACA"])
COL_GESTANTE = encontrar_coluna(["GESTANTE", "GRAVIDEZ", "GESTACAO"])
COL_DATA = encontrar_coluna(["DATA_NOTIFICACAO", "DATA_DE_NOTIFICACAO", "NOTIFICACAO", "DATA", "DATA_DO_CASO"])

# -------------------------------------------
# CRIAÇÃO DO MÊS + SEMANA EPIDEMIOLÓGICA
# -------------------------------------------
if COL_DATA:
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")
    df["MES"] = df[COL_DATA].dt.to_period("M").astype(str)
    df["SE_SEMANA"] = df[COL_DATA].dt.isocalendar().week.astype(str)
else:
    df["MES"] = "SEM_DATA"
    df["SE_SEMANA"] = "SEM_SE"

# -------------------------------------------
# FILTROS
# -------------------------------------------
st.sidebar.subheader("Filtros")

localidades = sorted(df[COL_LOCALIDADE].dropna().unique()) if COL_LOCALIDADE else []
classificacoes = sorted(df[COL_CLASSIFICACAO].dropna().unique()) if COL_CLASSIFICACAO else []
sexos = sorted(df[COL_SEXO].dropna().unique()) if COL_SEXO else []
racas = sorted(df[COL_RACA].dropna().unique()) if COL_RACA else []
semanas = sorted(df["SE_SEMANA"].dropna().unique())

f_localidade = st.sidebar.multiselect("Localidade", localidades)
f_classificacao = st.sidebar.multiselect("Classificação", classificacoes)
f_sexo = st.sidebar.multiselect("Sexo", sexos)
f_raca = st.sidebar.multiselect("Raça/Cor", racas)
f_se = st.sidebar.multiselect("Semana Epidemiológica", semanas)

df_filtrado = df.copy()

if f_localidade:
    df_filtrado = df_filtrado[df_filtrado[COL_LOCALIDADE].isin(f_localidade)]

if f_classificacao:
    df_filtrado = df_filtrado[df_filtrado[COL_CLASSIFICACAO].isin(f_classificacao)]

if f_sexo:
    df_filtrado = df_filtrado[df_filtrado[COL_SEXO].isin(f_sexo)]

if f_raca:
    df_filtrado = df_filtrado[df_filtrado[COL_RACA].isin(f_raca)]

if f_se:
    df_filtrado = df_filtrado[df_filtrado["SE_SEMANA"].isin(f_se)]

# -------------------------------------------
# INDICADORES
# -------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Total de Registros", len(df_filtrado))

with col2:
    if COL_GESTANTE:
        total_gest = df_filtrado[COL_GESTANTE].str.contains("SIM", case=False, na=False).sum()
        st.metric("Gestantes Identificadas", total_gest)
    else:
        st.metric("Gestantes Identificadas", "-")

# -------------------------------------------
# GRÁFICOS
# -------------------------------------------
st.subheader("📈 Casos por Mês")

fig_mes = px.bar(
    df_filtrado["MES"].value_counts().sort_index(),
    title="Casos por Mês",
    labels={"index": "Mês", "value": "Quantidade"}
)
st.plotly_chart(fig_mes, use_container_width=True)

if COL_GESTANTE:
    st.subheader("🤰 Gestantes")
    fig_g = px.pie(
        df_filtrado,
        names=COL_GESTANTE,
        title="Gestantes x Não Gestantes"
    )
    st.plotly_chart(fig_g, use_container_width=True)

if COL_CLASSIFICACAO:
    st.subheader("📊 Classificação por Mês")
    fig_class = px.histogram(
        df_filtrado, x="MES", color=COL_CLASSIFICACAO,
        barmode="group", title="Classificação por Mês"
    )
    st.plotly_chart(fig_class, use_container_width=True)

if COL_LOCALIDADE:
    st.subheader("📍 Casos por Localidade")
    fig_loc = px.histogram(
        df_filtrado, x=COL_LOCALIDADE, color=COL_CLASSIFICACAO,
        title="Classificação por Localidade", barmode="group"
    )
    st.plotly_chart(fig_loc, use_container_width=True)

# -------------------------------------------
# TABELA FINAL (SEM MES / SEM NASCIMENTO)
# -------------------------------------------
st.subheader("📋 Dados Filtrados")

df_exibicao = df_filtrado.drop(columns=["MES"], errors="ignore")
df_exibicao = df_exibicao[[c for c in df_exibicao.columns if "NASC" not in c.upper()]]

st.dataframe(df_exibicao, use_container_width=True)

st.caption("Desenvolvido por Maviael Barros.")
st.markdown("---")
st.caption("Painel de Oropouche • Versão 1.0")
