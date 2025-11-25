# 4_localidades.py
# Dashboard de Localidades – VISA Ipojuca

import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Programa de Controle da Esquistossomose",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Programa de Controle da Esquistossomose – Análise por Localidade")

# ---------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------

def normalize(text):
    """Normaliza: remove acentos, deixa maiúsculo e troca espaços por _"""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text.replace(" ", "_").upper()


def detectar_coluna(df, candidatos):
    """Encontra automaticamente a coluna correta."""
    cols = {normalize(c): c for c in df.columns}
    for c in candidatos:
        c_norm = normalize(c)
        if c_norm in cols:
            return cols[c_norm]
    return None


def converter_para_csv(url):
    """Transforma link padrão do Google Sheets em link CSV."""
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    except:
        return None


# ---------------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------------

@st.cache_data
def carregar_dados():
    url_original = "https://docs.google.com/spreadsheets/d/15Z5rsBKKY5nX2mi8Zn1u18IGcTsQ0o_E/edit?usp=sharing"
    url_csv = converter_para_csv(url_original)

    if not url_csv:
        st.error("❌ URL inválida.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(url_csv, dtype=str)
    except Exception as e:
        st.error(f"❌ Erro ao carregar a planilha: {e}")
        return pd.DataFrame()

    df.columns = [c.strip() for c in df.columns]
    return df


df = carregar_dados()

if df.empty:
    st.stop()

# ---------------------------------------------------------
# IDENTIFICAÇÃO DE COLUNAS
# ---------------------------------------------------------

COL_LOCALIDADE = detectar_coluna(df, ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO"])
COL_DATA = detectar_coluna(df, ["DATA", "DATA_REGISTRO", "DT", "DATA_OCORRENCIA"])

# Converter data, se existir
if COL_DATA:
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors="coerce")

# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------

st.sidebar.header("🔎 Filtros")

df_filtrado = df.copy()

# Filtro de localidade
if COL_LOCALIDADE:
    localidades = sorted(df[COL_LOCALIDADE].dropna().unique())
    sel_loc = st.sidebar.multiselect("Localidade", localidades, default=localidades)
    df_filtrado = df_filtrado[df_filtrado[COL_LOCALIDADE].isin(sel_loc)]

# Filtro temporal (opcional)
if COL_DATA:
    min_d = df_filtrado[COL_DATA].min()
    max_d = df_filtrado[COL_DATA].max()

    data_ini, data_fim = st.sidebar.date_input(
        "Período",
        value=[min_d, max_d]
    )

    df_filtrado = df_filtrado[
        (df_filtrado[COL_DATA] >= pd.to_datetime(data_ini)) &
        (df_filtrado[COL_DATA] <= pd.to_datetime(data_fim))
    ]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ---------------------------------------------------------
# INDICADORES RÁPIDOS
# ---------------------------------------------------------

st.header("📊 Indicadores Gerais")

col1, col2 = st.columns(2)

col1.metric("Registros filtrados", len(df_filtrado))

if COL_LOCALIDADE:
    top_loc = df_filtrado[COL_LOCALIDADE].value_counts().idxmax()
    col2.metric("Localidade mais frequente", top_loc)

# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------

st.header("📈 Análises Gráficas")

# Gráfico de barras – Localidade
if COL_LOCALIDADE:
    df_loc = df_filtrado[COL_LOCALIDADE].value_counts().reset_index()
    df_loc.columns = ["Localidade", "Quantidade"]

    fig = px.bar(
        df_loc,
        x="Localidade",
        y="Quantidade",
        title="Distribuição de Registros por Localidade",
        color="Quantidade",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de pizza – Localidade
if COL_LOCALIDADE:
    fig = px.pie(
        df_loc,
        names="Localidade",
        values="Quantidade",
        title="Proporção por Localidade"
    )
    st.plotly_chart(fig, use_container_width=True)

# Linha temporal
if COL_DATA:
    df_temp = df_filtrado.groupby(COL_DATA).size().reset_index(name="Quantidade")

    fig = px.line(
        df_temp,
        x=COL_DATA,
        y="Quantidade",
        markers=True,
        title="Evolução temporal dos registros"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TABELA FINAL – APENAS AS COLUNAS ESPECIFICADAS
# ---------------------------------------------------------

st.header("📋 Dados Filtrados")

# Detectar automaticamente colunas equivalentes
mapa_colunas = {
    "LOCALIDADE": ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO"],
    "EXAMES": ["EXAMES", "TOTAL_EXAMES", "N_EXAMES"],
    "A TRATAR": ["A_TRATAR", "A TRATAR", "N_A_TRATAR"],
    "TRATADOS": ["TRATADOS", "N_TRATADOS"],
    "POSITIVOS": ["POSITIVOS", "CASOS_POSITIVOS", "TESTES_POSITIVOS"],
    "POP. TRAB": ["POP_TRAB", "POP. TRAB.", "POP_TRABALHADORES", "POP TRAB"]
}

def encontrar_coluna(df, lista_nomes):
    """Retorna a coluna presente no DataFrame dentre as opções possíveis."""
    lista_normalizada = [normalize(c) for c in df.columns]

    for nome in lista_nomes:
        nome_norm = normalize(nome)
        for i, col_df in enumerate(df.columns):
            if normalize(col_df) == nome_norm:
                return col_df
    return None

# Selecionar apenas as colunas desejadas
colunas_finais = []

for alvo, candidatos in mapa_colunas.items():
    coluna_encontrada = encontrar_coluna(df_filtrado, candidates if (candidates := candidatos) else [])
    if coluna_encontrada:
        colunas_finais.append(coluna_encontrada)

# Garantir que só as colunas desejadas apareçam
df_visivel = df_filtrado[colunas_finais].copy()

st.dataframe(df_visivel, use_container_width=True)

st.markdown("---")
st.caption("Dashboard por PCE • Vigilância em Saúde Ipojuca")

st.caption("Desenvolvido por Maviael Barros.")
st.markdown("---")
st.caption("Painel do Programa de Controle da Esquistossomose • Versão 1.0")
