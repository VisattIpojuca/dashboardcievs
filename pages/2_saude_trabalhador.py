import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata

# ------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------------
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

st.title("👷 Saúde do Trabalhador – Análise dos Acidentes de Trabalho")
st.caption("Fonte: Vigilância em Saúde do Trabalhador – Ipojuca")

# ------------------------------------------------------
# FUNÇÃO PARA LIMPAR NOMES DE COLUNAS
# ------------------------------------------------------
def limpar_coluna(col):
    col = str(col)
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = col.strip().upper().replace(" ", "_").replace("-", "_").replace("/", "_")
    return col

# ------------------------------------------------------
# CARREGAR BASE REAL DO GOOGLE SHEETS
# ------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"

    try:
        df = pd.read_csv(url)
    except:
        st.error("❌ Erro ao carregar a planilha. Verifique o link ou permissões.")
        st.stop()

    df.columns = [limpar_coluna(c) for c in df.columns]

    # Coluna oficial de data
    if "DATA_DE_OCORRENCIA" in df.columns:
        df["DATA_DE_OCORRENCIA"] = pd.to_datetime(df["DATA_DE_OCORRENCIA"], errors="coerce")

    return df

df = carregar_dados()

if df.empty:
    st.warning("A base está vazia.")
    st.stop()

# ------------------------------------------------------
# FILTROS
# ------------------------------------------------------
st.sidebar.header("Filtros")

df_filtrado = df.copy()

def criar_filtro(coluna, label=None, ordenar=False):
    if coluna in df_filtrado.columns:
        opcoes = df_filtrado[coluna].dropna().unique().tolist()
        if ordenar:
            opcoes = sorted(opcoes)
        selecao = st.sidebar.multiselect(label or coluna, opcoes)
        if selecao:
            return df_filtrado[df_filtrado[coluna].isin(selecao)]
    return df_filtrado

df_filtrado = criar_filtro("SEMANA_EPIDEMIOLOGICA", "Semana Epidemiológica", ordenar=True)
df_filtrado = criar_filtro("IDADE", "Idade", ordenar=True)
df_filtrado = criar_filtro("SEXO", "Sexo")
df_filtrado = criar_filtro("RACA_COR", "Raça/Cor", ordenar=True)
df_filtrado = criar_filtro("ESCOLARIDADE", "Escolaridade", ordenar=True)
df_filtrado = criar_filtro("OCUPACAO", "Ocupação", ordenar=True)
df_filtrado = criar_filtro("SITUACAO_NO_MERCADO_DE_TRABALHO", "Situação no Mercado de Trabalho", ordenar=True)
df_filtrado = criar_filtro("BAIRRO_OCORRENCIA", "Bairro de Ocorrência", ordenar=True)
df_filtrado = criar_filtro("EVOLUCAO_DO_CASO", "Evolução do Caso", ordenar=True)

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros aplicados.")
    st.stop()

# ------------------------------------------------------
# INDICADORES PRINCIPAIS
# ------------------------------------------------------
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

# Total
total = len(df_filtrado)

# Média semanal
if "DATA_DE_OCORRENCIA" in df_filtrado.columns:
    df_sem = df_filtrado.groupby(pd.Grouper(key="DATA_DE_OCORRENCIA", freq="W")).size()
    media_semanal = round(df_sem.mean(), 2)
else:
    media_semanal = "—"

# Ocupação mais afetada
if "OCUPACAO" in df_filtrado.columns:
    ocup_mais = df_filtrado["OCUPACAO"].value_counts().idxmax()
else:
    ocup_mais = "Não informado"

# Óbitos
if "EVOLUCAO_DO_CASO" in df_filtrado.columns:
    obitos = df_filtrado["EVOLUCAO_DO_CASO"].astype(str).str.contains("ÓBITO", case=False).sum()
else:
    obitos = 0

with col1:
    st.metric("Total de Registros", total)

with col2:
    st.metric("Média Semanal", media_semanal)

with col3:
    st.metric("Ocupação mais acometida", ocup_mais)

with col4:
    st.metric("Óbitos", obitos)

# ------------------------------------------------------
# EVOLUÇÃO TEMPORAL
# ------------------------------------------------------
st.header("📈 Evolução Temporal dos Acidentes")

if "DATA_DE_OCORRENCIA" in df_filtrado.columns:
    df_temp = df_filtrado.groupby("DATA_DE_OCORRENCIA").size().reset_index(name="Casos")

    fig_temp = px.line(
        df_temp,
        x="DATA_DE_OCORRENCIA",
        y="Casos",
        markers=True,
        title="Evolução dos Acidentes (Data de ocorrência)"
    )
    st.plotly_chart(fig_temp, use_container_width=True)
else:
    st.info("⚠ A base não possui coluna DATA_DE_OCORRENCIA.")

# ------------------------------------------------------
# GRÁFICOS DE PERFIL (IDADE, SEXO, RAÇA/COR, ESCOLARIDADE)
# ------------------------------------------------------

st.header("👥 Perfil dos Trabalhadores Notificados")

colA, colB = st.columns(2)

# Sexo
if "SEXO" in df_filtrado.columns:
    fig_sexo = px.pie(
        df_filtrado,
        names="SEXO",
        title="Distribuição por Sexo"
    )
    colA.plotly_chart(fig_sexo, use_container_width=True)

# Idade
if "IDADE" in df_filtrado.columns:
    fig_idade = px.histogram(
        df_filtrado,
        x="IDADE",
        nbins=20,
        title="Distribuição de Idade"
    )
    colB.plotly_chart(fig_idade, use_container_width=True)

# Raça/cor
if "RACA_COR" in df_filtrado.columns:
    st.subheader("📊 Raça/Cor")
    fig_raca = px.bar(
        df_filtrado["RACA_COR"].value_counts().reset_index(),
        x="index",
        y="RACA_COR",
        labels={"index": "Raça/Cor", "RACA_COR": "Casos"},
        color="RACA_COR",
        title="Distribuição por Raça/Cor"
    )
    st.plotly_chart(fig_raca, use_container_width=True)

# Escolaridade
if "ESCOLARIDADE" in df_filtrado.columns:
    st.subheader("🎓 Escolaridade")
    fig_esc = px.bar(
        df_filtrado["ESCOLARIDADE"].value_counts().reset_index(),
        x="index",
        y="ESCOLARIDADE",
        labels={"index": "Escolaridade", "ESCOLARIDADE": "Casos"},
        color="ESCOLARIDADE",
        title="Distribuição por Escolaridade"
    )
    st.plotly_chart(fig_esc, use_container_width=True)

# ------------------------------------------------------
# BAIRRO E EVOLUÇÃO DO CASO
# ------------------------------------------------------

st.header("📍 Local e Evolução")

colC, colD = st.columns(2)

# Bairro
if "BAIRRO_OCORRENCIA" in df_filtrado.columns:
    df_bairro = df_filtrado["BAIRRO_OCORRENCIA"].value_counts().reset_index()
    df_bairro.columns = ["Bairro", "Casos"]

    fig_bairro = px.bar(
        df_bairro,
        x="Bairro",
        y="Casos",
        title="Casos por Bairro de Ocorrência",
        color="Casos"
    )
    colC.plotly_chart(fig_bairro, use_container_width=True)

# Evolução
if "EVOLUCAO_DO_CASO" in df_filtrado.columns:
    df_evo = df_filtrado["EVOLUCAO_DO_CASO"].value_counts().reset_index()
    df_evo.columns = ["Evolução", "Casos"]

    fig_evo = px.bar(
        df_evo,
        x="Evolução",
        y="Casos",
        title="Evolução dos Casos",
        color="Casos"
    )
    colD.plotly_chart(fig_evo, use_container_width=True)

# ------------------------------------------------------
# TABELA FINAL
# ------------------------------------------------------
st.header("📋 Base Filtrada")
st.dataframe(df_filtrado, use_container_width=True)

st.markdown("---")
st.caption("Painel de Saúde do Trabalhador – Ipojuca")
