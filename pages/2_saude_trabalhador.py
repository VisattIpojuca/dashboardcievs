import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata

# ----------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

st.title("👷 Saúde do Trabalhador - Análise de Acidentes de Trabalho")
st.caption("Fonte: Vigilância em Saúde do Trabalhador - Ipojuca")

# ----------------------------------------------------
# FUNÇÃO PARA PADRONIZAR NOMES DE COLUNAS
# ----------------------------------------------------
def limpar_coluna(col):
    col = str(col)
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = col.strip().upper().replace(" ", "_").replace("-", "_").replace("/", "_")
    return col

# ----------------------------------------------------
# CARREGAR BASE REAL DO GOOGLE SHEETS
# ----------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"

    try:
        df = pd.read_csv(url)
    except:
        st.error("❌ Erro ao carregar a planilha. Verifique o link ou permissões.")
        st.stop()

    df.columns = [limpar_coluna(c) for c in df.columns]

    # Converte colunas de data
    for coluna in ["DATA", "DATA_ACIDENTE", "DATA_NOTIFICACAO"]:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna], errors="coerce")

    return df

df = carregar_dados()

if df.empty:
    st.warning("A base está vazia.")
    st.stop()

# ----------------------------------------------------
# FILTROS AVANÇADOS
# ----------------------------------------------------
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

# 🔥 Filtros solicitados
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

# ----------------------------------------------------
# INDICADORES PRINCIPAIS
# ----------------------------------------------------
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

# Total de registros filtrados
total = len(df_filtrado)

setor_col = None
for col in df.columns:
    if "SETOR" in col:
        setor_col = col

if setor_col:
    setor_mais = df_filtrado[setor_col].value_counts().idxmax()
else:
    setor_mais = "Não informado"

with col1:
    st.metric("Registros", total)

with col2:
    if "DATA" in df_filtrado.columns:
        df_por_dia = df_filtrado.groupby("DATA").size()
        st.metric("Média Diária", round(df_por_dia.mean(), 2))
    else:
        st.metric("Média Diária", "—")

with col3:
    st.metric("Setor com mais notificações", setor_mais)

with col4:
    if "EVOLUCAO_DO_CASO" in df_filtrado.columns:
        obitos = (df_filtrado["EVOLUCAO_DO_CASO"].astype(str).str.contains("ÓBITO", case=False)).sum()
        st.metric("Óbitos", obitos)
    else:
        st.metric("Óbitos", "—")

# ----------------------------------------------------
# GRÁFICO TEMPORAL
# ----------------------------------------------------
st.header("📈 Evolução Temporal dos Acidentes")

if "DATA" in df_filtrado.columns:
    df_temp = df_filtrado.groupby("DATA").size().reset_index(name="Casos")

    fig = px.line(
        df_temp,
        x="DATA",
        y="Casos",
        markers=True,
        title="Casos ao Longo do Tempo"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("⚠ A base não contém coluna de DATA para análise temporal.")

# ----------------------------------------------------
# ANÁLISE POR BAIRRO
# ----------------------------------------------------
if "BAIRRO_OCORRENCIA" in df_filtrado.columns:
    st.header("📍 Distribuição por Bairro")

    df_bairro = df_filtrado["BAIRRO_OCORRENCIA"].value_counts().reset_index()
    df_bairro.columns = ["Bairro", "Casos"]

    fig_bairro = px.bar(
        df_bairro,
        x="Bairro",
        y="Casos",
        title="Casos por Bairro",
        color="Casos",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_bairro, use_container_width=True)

# ----------------------------------------------------
# ANÁLISE POR OCUPAÇÃO
# ----------------------------------------------------
if "OCUPACAO" in df_filtrado.columns:
    st.header("🛠 Ocupações mais afetadas")

    df_ocup = df_filtrado["OCUPACAO"].value_counts().reset_index()
    df_ocup.columns = ["Ocupação", "Casos"]

    fig_ocup = px.bar(
        df_ocup,
        x="Ocupação",
        y="Casos",
        title="Casos por Ocupação",
        color="Casos",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_ocup, use_container_width=True)

# ----------------------------------------------------
# TABELA FINAL
# ----------------------------------------------------
st.header("📋 Base Filtrada")
st.dataframe(df_filtrado, use_container_width=True)

st.markdown("---")
st.caption("Painel de Saúde do Trabalhador - Ipojuca")
