import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import unicodedata
from datetime import datetime

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# PALETA DE CORES — PADRÃO INSTITUCIONAL
# (ALINHADA COM O DASHBOARD DE DENGUE)
# ==========================================================
CORES = {
    "azul": "#004A8D",       # azul principal
    "azul_sec": "#0073CF",   # azul secundário
    "verde": "#009D4A",      # verde institucional
    "amarelo": "#FFC20E",    # amarelo institucional
    "cinza_claro": "#F2F2F2",
    "branco": "#FFFFFF"
}

PALETA = [
    CORES["azul"],
    CORES["verde"],
    CORES["amarelo"]
]

# ==========================================================
# FUNÇÕES AUXILIARES DE TEXTO/COLUNAS
# ==========================================================

def normalize(text):
    """Normaliza texto para comparação (sem acento, maiúsculo, com underscore)."""
    if pd.isna(text):
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.replace(" ", "_").upper()


def remover_acentos(texto: str) -> str:
    """Remove acentos de um texto (útil para 'ÓBITO'/'OBITO')."""
    return unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("utf-8")


def detectar_coluna(df, termos):
    """Detecta coluna do DataFrame que contenha algum dos termos normalizados."""
    cols_norm = {normalize(c): c for c in df.columns}
    for alvo in termos:
        alvo_norm = normalize(alvo)
        for col_norm, original in cols_norm.items():
            if alvo_norm in col_norm:
                return original
    return None


def contar_obitos(df, coluna):
    """Conta óbitos a partir da coluna de evolução, usando vários padrões."""
    if not coluna or coluna not in df.columns:
        return 0

    padroes = [
        "OBITO POR ACIDENTE DE TRABALHO GRAVE",
        "OBITO",
        "MORTE",
        "FALEC"
    ]

    serie = df[coluna].astype(str).str.upper().apply(remover_acentos)

    resultados = pd.DataFrame({
        p: serie.str.contains(p, case=False, na=False)
        for p in padroes
    })

    return resultados.any(axis=1).sum()


# ==========================================================
# CSS — ALINHADO AO DASHBOARD DE DENGUE
# ==========================================================

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

    /* Texto principal */
    body, p, li, span, label, .stMarkdown {{
        color: #0073CF !important;
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
    }}

    /* Fundo geral */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--azul-principal) !important;
    }}
    [data-testid="stSidebar"] a {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 600;
    }}

    /* TEXTO E CAMPOS DOS FILTROS – tema claro (padrão azul escuro) */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stMultiSelect * {{
        color: {CORES["azul"]} !important;
    }}

    /* Campo de período (DateInput) com texto azul claro */
    [data-testid="stSidebar"] .stDateInput input {{
        color: {CORES["azul_sec"]} !important;
    }}

    /* Campos de texto, número, select e multiselect: fundo branco */
    [data-testid="stSidebar"] .stTextInput > div > div,
    [data-testid="stSidebar"] .stNumberInput > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {{
        background-color: var(--branco) !important;
        border-radius: 6px !important;
    }}

    /* DateInput (Período) mantém fundo branco, só mudamos a cor da fonte */
    [data-testid="stSidebar"] .stDateInput > div > div {{
        background-color: var(--branco) !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {{
        color: #2f6bbd !important;
    }}

    /* OPÇÕES SELECIONADAS (chips) */
    [data-testid="stSidebar"] .stMultiSelect div[aria-selected="true"],
    [data-testid="stSidebar"] .stSelectbox div[aria-selected="true"] {{
        background-color: {CORES["verde"]} !important;
        color: white !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"],
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] * {{
        background-color: {CORES["verde"]} !important;
        color: white !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stTextInput > div,
    [data-testid="stSidebar"] .stNumberInput > div,
    [data-testid="stSidebar"] .stDateInput > div {{
        border-color: var(--azul-secundario) !important;
        border-radius: 6px !important;
    }}

    /* GRÁFICOS – garantir fundo branco */
    .js-plotly-plot .plotly .bg,
    .js-plotly-plot .plotly .plotly-background,
    .js-plotly-plot .plotly .paper,
    .js-plotly-plot .plotly .plotbg {{
        fill: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }}

    /* Textos dentro dos gráficos: forçar cor em azul escuro mesmo no modo escuro do navegador */
    .js-plotly-plot text {{
        fill: {CORES["azul"]} !important;
        color: {CORES["azul"]} !important;
    }}

    /* Borda preta externa em todos os gráficos Plotly */
    .element-container .js-plotly-plot {{
        border: 1px solid #000000 !important;
        border-radius: 4px !important;
        padding: 4px !important;
        background-color: #FFFFFF !important;
    }}

    /* MENU PÁGINAS NA SIDEBAR */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button[aria-current="page"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }}

    /* ===========================
       MODO ESCURO: DROPDOWN azul claro + texto branco
       =========================== */
    @media (prefers-color-scheme: dark) {{

        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] .stMultiSelect,
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stNumberInput,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stDateInput,
        [data-testid="stSidebar"] .stTextInput,
        [data-testid="stSidebar"] .stMultiSelect * {{
            color: #FFFFFF !important;
        }}

        /* No modo escuro, o texto do Período também fica branco para contraste */
        [data-testid="stSidebar"] .stDateInput input {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"],
        [data-testid="stSidebar"] ul[role="listbox"] {{
            background-color: {CORES["azul_sec"]} !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"] *,
        [data-testid="stSidebar"] ul[role="listbox"] * {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="option"],
        [data-testid="stSidebar"] li[role="option"] {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="option"][aria-selected="true"],
        [data-testid="stSidebar"] li[role="option"][aria-selected="true"] {{
            background-color: rgba(0,0,0,0.2) !important;
            color: #FFFFFF !important;
        }}
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
        color: #FFFFFF !important;
        background-color: var(--cinza-claro) !important;
        border-radius: 6px !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# TEMA DOS GRÁFICOS PLOTLY – FUNDO BRANCO, TEXTO/LINHAS AZUL ESCURO
# ==========================================================

def aplicar_tema_plotly(fig):
    """
    - fundo branco;
    - todos os textos em azul escuro (títulos, eixos, legenda, textos internos).
    """
    azul_escuro = CORES["azul"]

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font=dict(color=azul_escuro),

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            zerolinecolor="rgba(0,0,0,0.6)",
            color=azul_escuro,
            title_font=dict(color=azul_escuro)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            zerolinecolor="rgba(0,0,0,0.6)",
            color=azul_escuro,
            title_font=dict(color=azul_escuro)
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.3)",
            borderwidth=1,
            font=dict(color=azul_escuro)
        ),

        title_font=dict(color=azul_escuro),
        margin=dict(l=60, r=40, t=60, b=60)
    )

    # Textos internos das séries, se existirem
    try:
        fig.update_traces(textfont=dict(color=azul_escuro))
    except Exception:
        pass

    # Contornos em barras/histogramas
    try:
        fig.update_traces(marker_line_color="rgba(0,0,0,0.3)")
    except Exception:
        pass

    return fig


# ==========================================================
# CARREGAR DADOS
# ==========================================================

@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1Guru662qCn9bX8iZhckcbRu2nG8my4Eu5l5JK5yTNik/export?format=csv"
    df = pd.read_csv(url, dtype=str)

    # Normaliza colunas (mantendo sua lógica original)
    df.columns = [normalize(c) for c in df.columns]
    df.columns = [c.replace("__", "_") for c in df.columns]
    df.columns = [c.replace("_", " ") for c in df.columns]

    return df


# ==========================================================
# FILTROS
# ==========================================================

def aplicar_filtros(df, col_data, col_semana, col_sexo, col_idade,
                    col_raca, col_escolaridade, col_bairro,
                    col_ocupacao, col_situacao, col_evol):

    st.sidebar.header("🔎 Filtros")
    df_filtrado = df.copy()

    # Período
    min_d, max_d = df_filtrado[col_data].min(), df_filtrado[col_data].max()

    data_ini, data_fim = st.sidebar.date_input(
        "Período",
        value=[min_d, max_d],
        min_value=min_d,
        max_value=max_d
    )

    df_filtrado = df_filtrado[
        (df_filtrado[col_data] >= pd.to_datetime(data_ini)) &
        (df_filtrado[col_data] <= pd.to_datetime(data_fim))
    ]

    # Semana epidemiológica
    if col_semana:
        semanas = df[col_semana].dropna().astype(str).str.extract(r"(\d+)")[0]
        semanas = semanas.dropna().astype(int).unique()
        semanas = sorted(semanas)

        semanas_sel = st.sidebar.multiselect("Semana Epidemiológica", semanas)

        if semanas_sel:
            semanas_df = df_filtrado[col_semana].astype(str).str.extract(r"(\d+)")[0].astype(float)
            df_filtrado = df_filtrado[semanas_df.isin(semanas_sel)]

    # Multiselect genérico
    def add_filtro(label, coluna):
        nonlocal df_filtrado
        if coluna:
            opcoes = sorted(df[coluna].dropna().unique())
            escolhidos = st.sidebar.multiselect(label, opcoes)
            if escolhidos:
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(escolhidos)]

    add_filtro("Sexo", col_sexo)
    add_filtro("Idade", col_idade)
    add_filtro("Raça/Cor", col_raca)
    add_filtro("Escolaridade", col_escolaridade)
    add_filtro("Ocupação", col_ocupacao)
    add_filtro("Situação no Mercado de Trabalho", col_situacao)
    add_filtro("Bairro de Ocorrência", col_bairro)
    add_filtro("Evolução do Caso", col_evol)

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        st.stop()

    return df_filtrado


# ==========================================================
# INDICADORES
# ==========================================================

def mostrar_indicadores(df_filtrado, col_ocupacao, col_evol):
    st.header("📊 Indicadores Principais")

    total = len(df_filtrado)
    obitos = contar_obitos(df_filtrado, col_evol)
    if col_ocupacao and col_ocupacao in df_filtrado.columns and not df_filtrado[col_ocupacao].dropna().empty:
        top_ocup = df_filtrado[col_ocupacao].value_counts().idxmax()
    else:
        top_ocup = "Indefinido"

    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Acidentes", total)
    c2.metric("Óbitos", obitos)
    c3.metric("Ocupação mais afetada", top_ocup)


# ==========================================================
# GRÁFICOS
# ==========================================================

def mostrar_graficos(df_filtrado, col_sexo, col_raca, col_idade,
                     col_escolaridade, col_bairro, col_evol):
    st.header("📈 Distribuições")

    # Sexo
    if col_sexo:
        ds = df_filtrado[col_sexo].value_counts().reset_index()
        ds.columns = ["SEXO", "QTD"]
        fig = px.pie(
            ds,
            names="SEXO",
            values="QTD",
            hole=0.3,
            title="Distribuição por Sexo",
            color_discrete_sequence=PALETA
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Raça × Sexo
    if col_raca and col_sexo:
        d = df_filtrado[[col_raca, col_sexo]].dropna()
        d = d.groupby([col_raca, col_sexo]).size().reset_index(name="QTD")
        fig = px.bar(
            d,
            x=col_raca,
            y="QTD",
            color=col_sexo,
            barmode="group",
            title="Raça/Cor por Sexo",
            color_discrete_sequence=PALETA
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Idade
    if col_idade:
        fig = px.histogram(
            df_filtrado,
            x=col_idade,
            title="Distribuição por Idade",
            color_discrete_sequence=[CORES["azul"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Escolaridade
    if col_escolaridade:
        df_esc = df_filtrado[col_escolaridade].value_counts().reset_index()
        df_esc.columns = ["ESCOLARIDADE", "QTD"]
        fig = px.bar(
            df_esc,
            x="ESCOLARIDADE",
            y="QTD",
            title="Escolaridade",
            color_discrete_sequence=[CORES["azul_sec"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Bairro
    if col_bairro:
        df_bairro = df_filtrado[col_bairro].value_counts().reset_index()
        df_bairro.columns = ["BAIRRO", "QTD"]
        fig = px.bar(
            df_bairro.head(20),
            x="BAIRRO",
            y="QTD",
            title="Top 20 Bairros",
            color_discrete_sequence=[CORES["verde"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Evolução
    if col_evol:
        df_ev = df_filtrado[col_evol].value_counts().reset_index()
        df_ev.columns = ["EVOLUCAO", "QTD"]
        fig = px.bar(
            df_ev,
            x="EVOLUCAO",
            y="QTD",
            title="Evolução dos Casos",
            color_discrete_sequence=[CORES["amarelo"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# MAIN
# ==========================================================

def main():
    aplicar_css()

    st.title("👷 Saúde do Trabalhador - Análise de Acidentes de Trabalho")

    # Carrega dados
    df = carregar_dados()
    if df.empty:
        st.warning("Nenhum dado encontrado.")
        st.stop()

    # Identificar colunas importantes
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

    COL_SEMANA = detectar_coluna(df, [
        "SEMANA", "EPID", "SE", "SEMANA_EPIDEMIOLOGICA", "SEM EPID"
    ])

    # Aplica filtros
    df_filtrado = aplicar_filtros(
        df, COL_DATA, COL_SEMANA, COL_SEXO, COL_IDADE,
        COL_RACA, COL_ESCOLARIDADE, COL_BAIRRO,
        COL_OCUPACAO, COL_SITUACAO, COL_EVOL
    )

    # Indicadores
    mostrar_indicadores(df_filtrado, COL_OCUPACAO, COL_EVOL)

    # Gráficos
    mostrar_graficos(
        df_filtrado, COL_SEXO, COL_RACA, COL_IDADE,
        COL_ESCOLARIDADE, COL_BAIRRO, COL_EVOL
    )

    # Tabela
    st.header("📋 Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

    st.markdown("---")
    st.caption("Painel de Saúde do Trabalhador • Versão 1.0 (tema institucional)")
    st.caption("Desenvolvido por Maviael Barros.")


if __name__ == "__main__":
    main()
