# 4_localidades.py
# Dashboard de Localidades – VISA Ipojuca (tema institucional)

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
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📍 Programa de Controle da Esquistossomose – Análise por Localidade")

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
# CSS – MESMO ESTILO DOS OUTROS PAINÉIS
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
        background-color: var(--cinza-claro) !important;
    }}
    </style>
    """, unsafe_allow_html=True)


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
    except Exception:
        return None


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


# Detectar automaticamente colunas equivalentes (para tabela final)
def encontrar_coluna(df, lista_nomes):
    """Retorna a coluna presente no DataFrame dentre as opções possíveis."""
    for col_df in df.columns:
        for nome in lista_nomes:
            if normalize(col_df) == normalize(nome):
                return col_df
    return None


# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------
def aplicar_filtros(df, col_localidade, col_data):
    st.sidebar.header("🔎 Filtros")

    df_filtrado = df.copy()

    # Filtro de localidade
    if col_localidade:
        localidades = sorted(df[col_localidade].dropna().unique())
        sel_loc = st.sidebar.multiselect("Localidade", localidades, default=localidades)
        if sel_loc:
            df_filtrado = df_filtrado[df_filtrado[col_localidade].isin(sel_loc)]

    # Filtro temporal
    if col_data:
        min_d = df_filtrado[col_data].min()
        max_d = df_filtrado[col_data].max()

        data_ini, data_fim = st.sidebar.date_input(
            "Período",
            value=[min_d, max_d]
        )

        df_filtrado = df_filtrado[
            (df_filtrado[col_data] >= pd.to_datetime(data_ini)) &
            (df_filtrado[col_data] <= pd.to_datetime(data_fim))
        ]

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        st.stop()

    return df_filtrado


# ---------------------------------------------------------
# INDICADORES
# ---------------------------------------------------------
def mostrar_indicadores(df_filtrado, col_localidade):
    st.header("📊 Indicadores Gerais")

    col1, col2 = st.columns(2)

    col1.metric("Registros filtrados", len(df_filtrado))

    if col_localidade and col_localidade in df_filtrado.columns:
        if not df_filtrado[col_localidade].dropna().empty:
            top_loc = df_filtrado[col_localidade].value_counts().idxmax()
        else:
            top_loc = "Indefinido"
        col2.metric("Localidade mais frequente", top_loc)


# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------
def mostrar_graficos(df_filtrado, col_localidade, col_data):
    st.header("📈 Análises Gráficas")

    # Gráfico de barras – Localidade
    if col_localidade:
        df_loc = df_filtrado[col_localidade].value_counts().reset_index()
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
        fig = px.pie(
            df_loc,
            names="Localidade",
            values="Quantidade",
            title="Proporção por Localidade",
            color_discrete_sequence=PALETA
        )
        st.plotly_chart(fig, use_container_width=True)

    # Linha temporal
    if col_data:
        df_temp = df_filtrado.groupby(col_data).size().reset_index(name="Quantidade")

        fig = px.line(
            df_temp,
            x=col_data,
            y="Quantidade",
            markers=True,
            title="Evolução temporal dos registros",
            color_discrete_sequence=[CORES["azul"]]
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# TABELA FINAL – APENAS AS COLUNAS ESPECIFICADAS
# ---------------------------------------------------------
def mostrar_tabela(df_filtrado):
    st.header("📋 Dados Filtrados")

    mapa_colunas = {
        "LOCALIDADE": ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO"],
        "EXAMES": ["EXAMES", "TOTAL_EXAMES", "N_EXAMES"],
        "A TRATAR": ["A_TRATAR", "A TRATAR", "N_A_TRATAR"],
        "TRATADOS": ["TRATADOS", "N_TRATADOS"],
        "POSITIVOS": ["POSITIVOS", "CASOS_POSITIVOS", "TESTES_POSITIVOS"],
        "POP. TRAB": ["POP_TRAB", "POP. TRAB.", "POP_TRABALHADORES", "POP TRAB"],
    }

    colunas_finais = []
    for alvo, candidatos in mapa_colunas.items():
        coluna_encontrada = encontrar_coluna(df_filtrado, candidatos)
        if coluna_encontrada and coluna_encontrada not in colunas_finais:
            colunas_finais.append(coluna_encontrada)

    if colunas_finais:
        df_visivel = df_filtrado[colunas_finais].copy()
    else:
        df_visivel = df_filtrado.copy()

    st.dataframe(df_visivel, use_container_width=True)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    aplicar_css()

    df = carregar_dados()
    if df.empty:
        st.stop()

    # IDENTIFICAÇÃO DE COLUNAS
    col_localidade = detectar_coluna(df, ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO"])
    col_data = detectar_coluna(df, ["DATA", "DATA_REGISTRO", "DT", "DATA_OCORRENCIA"])

    # Converter data, se existir
    if col_data and col_data in df.columns:
        df[col_data] = pd.to_datetime(df[col_data], errors="coerce")

    # FILTROS
    df_filtrado = aplicar_filtros(df, col_localidade, col_data)

    # INDICADORES
    mostrar_indicadores(df_filtrado, col_localidade)

    # GRÁFICOS
    mostrar_graficos(df_filtrado, col_localidade, col_data)

    # TABELA FINAL
    mostrar_tabela(df_filtrado)

    st.markdown("---")
    st.caption("Dashboard por PCE • Vigilância em Saúde Ipojuca")
    st.markdown("---")
    st.caption("Painel do Programa de Controle da Esquistossomose • Versão 1.0 (tema institucional)")
    st.caption("Desenvolvido por Maviael Barros.")


if __name__ == "__main__":
    main()
