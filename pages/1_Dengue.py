import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import unicodedata

# =======================================================
# CONFIGURAÇÃO DA PÁGINA 
# =======================================================
st.set_page_config(
    page_title="Dengue – Painel de Vigilância em Saúde Ipojuca",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================================================
# MAPEAMENTOS E PADRÕES
# =======================================================

FINAL_RENAME_MAP = {
    'SEMANA_EPIDEMIOLOGICA': 'SEMANA_EPIDEMIOLOGICA',
    'SEMANA_EPIDEMIOLOGICA_2': 'SEMANA_EPIDEMIOLOGICA',
    'DATA_NOTIFICACAO': 'DATA_NOTIFICACAO',
    'DATA_DE_NOTIFICACAO': 'DATA_NOTIFICACAO',
    'DATA_PRIMEIRO_SINTOMAS': 'DATA_SINTOMAS',
    'DATA_PRIMEIROS_SINTOMAS': 'DATA_SINTOMAS',
    'FA': 'FAIXA_ETARIA',
    'BAIRRO_RESIDENCIA': 'BAIRRO',
    'EVOLUCAO_DO_CASO': 'EVOLUCAO',
    'CLASSIFICACAO': 'CLASSIFICACAO_FINAL',
    'RACA_COR': 'RACA_COR',
    'ESCOLARIDADE': 'ESCOLARIDADE',
    'DISTRITO': 'DISTRITO'
}

ORDEM_FAIXA_ETARIA = [
    '1 a 4 anos', '5 a 9 anos', '10 a 14 anos', '15 a 19 anos',
    '20 a 39 anos', '40 a 59 anos', '60 anos ou mais', 'IGNORADO'
]

MAPEAMENTO_FAIXA_ETARIA = {
    '0 a 4': '1 a 4 anos', '1 a 4': '1 a 4 anos', '5 a 9': '5 a 9 anos',
    '10 a 14': '10 a 14 anos', '15 a 19': '15 a 19 anos',
    '20 a 29': '20 a 39 anos', '30 a 39': '20 a 39 anos',
    '40 a 49': '40 a 59 anos', '50 a 59': '40 a 59 anos',
    '60 a 69': '60 anos ou mais', '70 a 79': '60 anos ou mais',
    '80 ou mais': '60 anos ou mais', 'IGNORADO': 'IGNORADO'
}

CORES = {
    "azul": "#004A8D",
    "verde": "#009D4A",
    "amarelo": "#FFC20E",
    "azul_claro": "#0073CF"
}

SINTOMAS_E_COMORBIDADES = [
    "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "VOMITO", "NAUSEA",
    "DOR_COSTAS", "CONJUNTVITE", "ARTRITE", "ARTRALGIA", "PETEQUIAS",
    "LEUCOPENIA", "LACO", "DOR_RETRO", "DIABETES", "HEMATOLOGICAS",
    "HEPATOPATIAS", "RENAL", "HIPERTENSAO", "ACIDO_PEPT", "AUTO_IMUNE"
]


def limpar_nome_coluna(col: str) -> str:
    """Normaliza nomes de colunas: remove acentos, espaços, hífens etc."""
    c = unicodedata.normalize('NFKD', str(col)).encode('ascii', 'ignore').decode()
    return c.strip().upper().replace(" ", "_").replace("-", "_").replace("/", "_")


def remover_acentos(texto: str) -> str:
    """Remove acentos de um texto (útil para padronizar 'ÓBITO'/'OBITO')."""
    return unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("utf-8")


# =======================================================
# CSS — PALETA INSTITUCIONAL + MENU/FILTROS
# =======================================================

def aplicar_css():
    st.markdown(f"""
    <style>
    :root {{
        --azul-principal: {CORES["azul"]};
        --azul-secundario: {CORES["azul_claro"]};
        --verde-ipojuca: {CORES["verde"]};
        --amarelo-ipojuca: {CORES["amarelo"]};
        --cinza-claro: #F2F2F2;
        --branco: #FFFFFF;
    }}

    body, p, li, span, label, .stMarkdown {{
        color: #0073CF !important;
    }}

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 800 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
    }}

    [data-testid="stSidebar"] {{
        background: var(--azul-principal) !important;
    }}
    [data-testid="stSidebar"] a {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 600;
    }}

    /* TEXTO E CAMPOS DOS FILTROS – tema claro */
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

    [data-testid="stSidebar"] .stTextInput > div > div,
    [data-testid="stSidebar"] .stNumberInput > div > div,
    [data-testid="stSidebar"] .stDateInput > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {{
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

    /* MENU PÁGINAS */
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

        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"],
        [data-testid="stSidebar"] ul[role="listbox"] {{
            background-color: {CORES["azul_claro"]} !important;
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

    .stMetric {{
        background-color: var(--amarelo-ipojuca) !important;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid var(--azul-secundario);
        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
    }}

    button, .stButton button {{
        color: #FFFFFF !important;
        background-color: var(--cinza-claro) !important;
        border-radius: 6px !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# =======================================================
# TEMA DOS GRÁFICOS PLOTLY – FUNDO BRANCO, TEXTO/LINHAS AZUL ESCURO
# =======================================================

def aplicar_tema_plotly(fig):
    """
    - fundo branco;
    - todos os textos em azul escuro (títulos, eixos, legenda, textos internos).
    """
    azul_escuro = CORES["azul"]

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        # Fonte padrão de tudo
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

    # Textos internos das séries (quando existirem) também em azul escuro
    try:
        fig.update_traces(textfont=dict(color=azul_escuro))
    except Exception:
        pass

    # Contornos suaves em barras/histogramas
    try:
        fig.update_traces(marker_line_color="rgba(0,0,0,0.3)")
    except Exception:
        pass

    return fig


# =======================================================
# CARREGAMENTO DO DATASET
# =======================================================

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    url = (
        "https://docs.google.com/spreadsheets/d/"
        "1bdHetdGEXLgXv7A2aGvOaItKxiAuyg0Ip0UER1BjjOg/export?format=csv"
    )

    try:
        df = pd.read_csv(url, encoding="utf-8")
    except Exception:
        st.error("❌ Erro ao carregar os dados da planilha do Google Sheets.")
        st.stop()

    # Normaliza nomes das colunas
    df.columns = [limpar_nome_coluna(c) for c in df.columns]

    # Renomeia de acordo com o mapa final, apenas as que existirem
    rename_dict = {orig: dest for orig, dest in FINAL_RENAME_MAP.items() if orig in df.columns}
    df.rename(columns=rename_dict, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]

    # Padroniza FAIXA_ETARIA
    if 'FAIXA_ETARIA' in df.columns:
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].astype(str).str.strip()
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].replace(MAPEAMENTO_FAIXA_ETARIA)
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].fillna("IGNORADO")

    # Converte datas
    for col in ['DATA_NOTIFICACAO', 'DATA_SINTOMAS']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# =======================================================
# FILTROS — SIDEBAR
# =======================================================

def aplicar_filtros(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("🔎 Filtros")
    df_filtrado = df.copy()

    if 'CLASSIFICACAO_FINAL' in df.columns:
        opcoes = sorted(df['CLASSIFICACAO_FINAL'].dropna().unique())
        sel = st.sidebar.multiselect("Classificação Final", opcoes)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['CLASSIFICACAO_FINAL'].isin(sel)]

    if 'SEMANA_EPIDEMIOLOGICA' in df.columns:
        semanas = sorted(df['SEMANA_EPIDEMIOLOGICA'].dropna().unique())
        sel = st.sidebar.multiselect("Semana Epidemiológica", semanas)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['SEMANA_EPIDEMIOLOGICA'].isin(sel)]

    if 'SEXO' in df.columns:
        sexos = sorted(df['SEXO'].dropna().unique())
        sel = st.sidebar.multiselect("Sexo", sexos)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['SEXO'].isin(sel)]

    if 'FAIXA_ETARIA' in df.columns:
        faixas = st.sidebar.multiselect("Faixa Etária", ORDEM_FAIXA_ETARIA)
        if faixas:
            df_filtrado = df_filtrado[df_filtrado['FAIXA_ETARIA'].isin(faixas)]

    if 'EVOLUCAO' in df.columns:
        evolucoes = sorted(df['EVOLUCAO'].dropna().unique())
        sel = st.sidebar.multiselect("Evolução do Caso", evolucoes)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['EVOLUCAO'].isin(sel)]

    if 'ESCOLARIDADE' in df.columns:
        escs = sorted(df['ESCOLARIDADE'].dropna().unique())
        sel = st.sidebar.multiselect("Escolaridade", escs)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['ESCOLARIDADE'].isin(sel)]

    if 'BAIRRO' in df.columns:
        bairros = sorted(df['BAIRRO"].dropna().unique())
        sel = st.sidebar.multiselect("Bairro", bairros)
        if sel:
            df_filtrado = df_filtrado[df_filtrado['BAIRRO"].isin(sel)]

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    return df_filtrado


# =======================================================
# INDICADORES
# =======================================================

def mostrar_indicadores(df_filtrado: pd.DataFrame):
    st.header("📊 Indicadores Gerais")
    col1, col2, col3, col4 = st.columns(4)

    total = len(df_filtrado)
    col1.metric("Notificações no período", total)

    confirmados = descartados = obitos = 0

    if 'CLASSIFICACAO_FINAL' in df_filtrado.columns:
        classif = df_filtrado['CLASSIFICACAO_FINAL'].astype(str).str.upper().str.strip()
        confirmados = classif.isin(["DENGUE", "DENGUE COM SINAIS DE ALARME"]).sum()
        descartados = (classif == "DESCARTADO").sum()

        col2.metric("Confirmados", confirmados)
        col3.metric("Descartados", descartados)

    if 'EVOLUCAO' in df_filtrado.columns:
        evol = df_filtrado['EVOLUCAO'].astype(str).str.upper().apply(remover_acentos)
        obitos = evol.str.contains("OBITO").sum()
        let = (obitos / confirmados) * 100 if confirmados else 0
        col4.metric("Letalidade (%)", f"{let:.2f}% ({obitos} óbitos)")


# =======================================================
# GRÁFICOS
# =======================================================

def mostrar_graficos(df_filtrado: pd.DataFrame):
    st.subheader("📈 Análise Temporal e Territorial")
    colA, colB = st.columns(2)

    # Casos por semana epidemiológica
    if 'SEMANA_EPIDEMIOLOGICA' in df_filtrado.columns:
        semanal = (
            df_filtrado
            .groupby("SEMANA_EPIDEMIOLOGICA")
            .size()
            .reset_index(name="Casos")
            .sort_values("SEMANA_EPIDEMIOLOGICA")
        )
        fig = px.line(
            semanal,
            x="SEMANA_EPIDEMIOLOGICA",
            y="Casos",
            markers=True,
            title="Casos por Semana Epidemiológica",
            color_discrete_sequence=[CORES["azul"]]
        )
        fig = aplicar_tema_plotly(fig)
        colA.plotly_chart(fig, use_container_width=True)

    # Casos por distrito
    if 'DISTRITO' in df_filtrado.columns:
        d = df_filtrado['DISTRITO'].value_counts().reset_index()
        d.columns = ['Distrito', 'Casos']
        fig = px.bar(
            d,
            x="Distrito",
            y="Casos",
            title="Distribuição de Casos por Distrito",
            color_discrete_sequence=[CORES["verde"]]
        )
        fig = aplicar_tema_plotly(fig)
        colB.plotly_chart(fig, use_container_width=True)

    # Casos por bairro
    st.subheader("🏘️ Casos por Bairro")
    if 'BAIRRO' in df_filtrado.columns:
        b = df_filtrado['BAIRRO'].value_counts().reset_index()
        b.columns = ['Bairro', 'Casos']
        fig = px.bar(
            b.head(15),
            x="Bairro",
            y="Casos",
            title="Top 15 Bairros",
            color_discrete_sequence=[CORES["azul_claro"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Perfil Social
    st.subheader("🎓 Perfil Social")
    if 'RACA_COR' in df_filtrado.columns and 'ESCOLARIDADE' in df_filtrado.columns:
        cruz = df_filtrado.groupby(['RACA_COR', 'ESCOLARIDADE']).size().reset_index(name='Casos')
        fig = px.bar(
            cruz,
            x="RACA_COR",
            y="Casos",
            color="ESCOLARIDADE",
            barmode="group",
            title="Casos por Raça/Cor e Escolaridade",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Sintomas e comorbidades
    st.subheader("🩺 Sintomas e Comorbidades")
    dados = []
    for s in SINTOMAS_E_COMORBIDADES:
        colname = limpar_nome_coluna(s)
        if colname in df_filtrado.columns:
            ct = (df_filtrado[colname].astype(str).str.upper().str.strip() == "SIM").sum()
            if ct > 0:
                dados.append({"Item": s.replace("_", " ").capitalize(), "Casos": ct})

    if dados:
        df_s = pd.DataFrame(dados)
        fig = px.bar(
            df_s.sort_values("Casos"),
            x="Casos",
            y="Item",
            orientation='h',
            title="Frequência de Sintomas e Comorbidades",
            color_discrete_sequence=[CORES["amarelo"]]
        )
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Perfil Demográfico
    st.subheader("👥 Perfil Demográfico")
    if 'FAIXA_ETARIA' in df_filtrado.columns and 'SEXO' in df_filtrado.columns:
        ordem_plot = [f for f in ORDEM_FAIXA_ETARIA if f in df_filtrado['FAIXA_ETARIA'].unique()]
        fig = px.histogram(
            df_filtrado,
            x="FAIXA_ETARIA",
            color="SEXO",
            barmode="group",
            title="Casos por Faixa Etária e Sexo",
            color_discrete_sequence=[CORES["azul"], CORES["verde"]]
        )
        fig.update_xaxes(categoryorder="array", categoryarray=ordem_plot)
        fig = aplicar_tema_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)


# =======================================================
# DOWNLOAD
# =======================================================

def botao_download(df_filtrado: pd.DataFrame):
    st.download_button(
        "📥 Baixar dados filtrados (CSV)",
        df_filtrado.to_csv(index=False).encode("utf-8-sig"),
        file_name="dados_filtrados_dengue.csv",
        mime="text/csv"
    )


# =======================================================
# MAIN
# =======================================================

def main():
    aplicar_css()

    # Título da página
    st.title("🦟 Dashboard Vigilância das Arboviroses (Dengue)")
    st.caption("Fonte: Gerência de Promoção, Prevenção e Vigilância Epidemiológica 📊🗺️")

    # Carrega dados
    df = carregar_dados()

    if df.empty:
        st.warning("Nenhum dado encontrado.")
        st.stop()

    # Aplica filtros
    df_filtrado = aplicar_filtros(df)

    # Indicadores
    mostrar_indicadores(df_filtrado)

    # Gráficos
    mostrar_graficos(df_filtrado)

    # Download
    botao_download(df_filtrado)

    st.markdown("---")
    st.caption("Painel de Dengue • Versão 1.0 (refatorada)")
    st.caption("Desenvolvido por Maviael Barros.")


if __name__ == "__main__":
    main()
