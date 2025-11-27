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
# CSS – MESMO ESTILO DOS OUTROS PAINÉIS (MENU PADRÃO)
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

    /* Texto principal da área central */
    [data-testid="stAppViewContainer"] body,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] .stMarkdown {{
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
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li {{
        text-align: justify !important;
    }}

    /* Fundo geral */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
    }}

    /* Sidebar (fundo azul) */
    [data-testid="stSidebar"] {{
        background: var(--azul-principal) !important;
    }}
    [data-testid="stSidebar"] a {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 600;
    }}

    /* MENU DE NAVEGAÇÃO */
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

    /* Título "Filtros" na sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {{
        color: var(--amarelo-ipojuca) !important;
        font-weight: 800 !important;
    }}

    /* RÓTULOS DOS FILTROS – AZUL CLARO */
    [data-testid="stSidebar"] div[class*="stMarkdown"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stTextInput label {{
        color: {CORES["azul_sec"]} !important;
        font-weight: 600 !important;
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

    /* Campos: fundo branco no modo claro */
    [data-testid="stSidebar"] .stTextInput > div > div,
    [data-testid="stSidebar"] .stNumberInput > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div,
    [data-testid="stSidebar"] .stDateInput > div > div {{
        background-color: var(--branco) !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {{
        color: #2f6bbd !important;
    }}

    /* Chips/opções selecionadas em multiselect (fundo verde, texto branco) */
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

    /* Borda dos campos de filtro em azul */
    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stTextInput > div,
    [data-testid="stSidebar"] .stNumberInput > div,
    [data-testid="stSidebar"] .stDateInput > div {{
        border-color: {CORES["azul_sec"]} !important;
        border-radius: 6px !important;
    }}

    /* GRÁFICOS – CSS de segurança */
    .js-plotly-plot .plotly .bg,
    .js-plotly-plot .plotly .plotly-background,
    .js-plotly-plot .plotly .paper,
    .js-plotly-plot .plotly .plotbg {{
        fill: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }}
    .js-plotly-plot text {{
        fill: {CORES["azul"]} !important;
        color: {CORES["azul"]} !important;
    }}
    .element-container .js-plotly-plot {{
        border: 1px solid #000000 !important;
        border-radius: 4px !important;
        padding: 4px !important;
        background-color: #FFFFFF !important;
    }}

    /* ===========================
       MODO ESCURO
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

        [data-testid="stSidebar"] div[class*="stMarkdown"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stNumberInput label,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stDateInput label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stTextInput label {{
            color: {CORES["azul_sec"]} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSidebar"] .stTextInput > div > div,
        [data-testid="stSidebar"] .stNumberInput > div > div,
        [data-testid="stSidebar"] .stSelectbox > div > div,
        [data-testid="stSidebar"] .stMultiSelect > div > div,
        [data-testid="stSidebar"] .stDateInput > div > div {{
            background-color: #1F2933 !important;
            border-radius: 6px !important;
        }}

        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {{
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] div[role="listbox"],
        [data-testid="stSidebar"] ul[role="listbox"] {{
            background-color: #1F2933 !important;
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

    # ----------------- Localidade -----------------
    if col_localidade:
        st.sidebar.markdown(
            f"<p style='margin-bottom:0px; margin-top:8px; "
            f"color:{CORES['azul_sec']}; font-weight:600; font-size:0.9rem;'>"
            f"Localidade</p>",
            unsafe_allow_html=True
        )

        localidades = sorted(df[col_localidade].dropna().unique())
        sel_loc = st.sidebar.multiselect(
            label="",
            options=localidades,
            default=localidades
        )
        if sel_loc:
            df_filtrado = df_filtrado[df_filtrado[col_localidade].isin(sel_loc)]

    # ----------------- Período (data) -----------------
    if col_data:
        df_filtrado[col_data] = pd.to_datetime(df_filtrado[col_data], errors="coerce")
        min_d = df_filtrado[col_data].min()
        max_d = df_filtrado[col_data].max()

        st.sidebar.markdown(
            f"<p style='margin-bottom:0px; margin-top:8px; "
            f"color:{CORES['azul_sec']}; font-weight:600; font-size:0.9rem;'>"
            f"Período</p>",
            unsafe_allow_html=True
        )

        data_ini, data_fim = st.sidebar.date_input(
            label="",
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
# INDICADORES – POP. TRAB, EXAMES, POSITIVOS, TRATADOS, A TRATAR
# ---------------------------------------------------------
def mostrar_indicadores(df_filtrado, col_localidade):
    st.header("📊 Indicadores Gerais")

    # Detectar colunas pelos mesmos padrões usados na tabela
    col_pop = encontrar_coluna(df_filtrado, ["POP_TRAB", "POP. TRAB.", "POP_TRABALHADORES", "POP TRAB"])
    col_exames = encontrar_coluna(df_filtrado, ["EXAMES", "TOTAL_EXAMES", "N_EXAMES"])
    col_positivos = encontrar_coluna(df_filtrado, ["POSITIVOS", "CASOS_POSITIVOS", "TESTES_POSITIVOS"])
    col_tratados = encontrar_coluna(df_filtrado, ["TRATADOS", "N_TRATADOS"])
    col_a_tratar = encontrar_coluna(df_filtrado, ["A_TRATAR", "A TRATAR", "N_A_TRATAR"])

    def soma_coluna(col):
        if col and col in df_filtrado.columns:
            return pd.to_numeric(df_filtrado[col], errors="coerce").sum()
        return 0

    total_pop = soma_coluna(col_pop)
    total_exames = soma_coluna(col_exames)
    total_positivos = soma_coluna(col_positivos)
    total_tratados = soma_coluna(col_tratados)
    total_a_tratar = soma_coluna(col_a_tratar)

    c1, c2, c3 = st.columns(3)
    c1.metric("População trabalhada ", int(total_pop) if pd.notna(total_pop) else "—")
    c2.metric("Exames realizados", int(total_exames) if pd.notna(total_exames) else "—")
    c3.metric("Positivos", int(total_positivos) if pd.notna(total_positivos) else "—")

    c4, c5, _ = st.columns(3)
    c4.metric("Tratados", int(total_tratados) if pd.notna(total_tratados) else "—")
    c5.metric("A tratar", int(total_a_tratar) if pd.notna(total_a_tratar) else "—")


# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------
def mostrar_graficos(df_filtrado, col_localidade, col_data):
    st.header("📈 Análises Gráficas")

    # Gráfico de barras – Localidade
    if col_localidade:
        df_loc = df_filtrado[col_localidade].value_counts().reset_index()
        df_loc.columns = ["Localidade", "Quantidade"]

        fig_bar = px.bar(
            df_loc,
            x="Localidade",
            y="Quantidade",
            title="Distribuição de Registros por Localidade",
            color="Quantidade",
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=CORES["azul"]),
            xaxis=dict(
                showgrid=False,
                linecolor="black",
                tickfont=dict(color=CORES["azul"])
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#DDDDDD",
                linecolor="black",
                tickfont=dict(color=CORES["azul"])
            ),
            legend=dict(font=dict(color=CORES["azul"]))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Gráfico de pizza – Localidade
        fig_pie = px.pie(
            df_loc,
            names="Localidade",
            values="Quantidade",
            title="Proporção por Localidade",
            color_discrete_sequence=PALETA
        )
        fig_pie.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=CORES["azul"]),
            legend=dict(font=dict(color=CORES["azul"]))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Linha temporal
    if col_data:
        df_temp = df_filtrado.groupby(col_data).size().reset_index(name="Quantidade")

        fig_line = px.line(
            df_temp,
            x=col_data,
            y="Quantidade",
            markers=True,
            title="Evolução temporal dos registros",
            color_discrete_sequence=[CORES["azul"]]
        )
        fig_line.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=CORES["azul"]),
            xaxis=dict(
                showgrid=False,
                linecolor="black",
                tickfont=dict(color=CORES["azul"])
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#DDDDDD",
                linecolor="black",
                tickfont=dict(color=CORES["azul"])
            ),
            legend=dict(font=dict(color=CORES["azul"]))
        )
        st.plotly_chart(fig_line, use_container_width=True)


# ---------------------------------------------------------
# TABELA FINAL – APENAS AS COLUNAS ESPECIFICADAS, SEM LINHA TOTAL
# ---------------------------------------------------------
def mostrar_tabela(df_filtrado):
    st.header("📋 Dados Filtrados")

    # Remover linha de TOTAL, se existir (ex.: na coluna de localidade)
    col_localidade = encontrar_coluna(df_filtrado, ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO"])
    if col_localidade and col_localidade in df_filtrado.columns:
        df_filtrado = df_filtrado[
            ~df_filtrado[col_localidade].astype(str).str.upper().str.strip().isin(
                ["TOTAL", "TOTAL GERAL", "TOTALGERAL"]
            )
        ]

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
    st.caption("Painel do Programa de Controle da Esquistossomose • Versão 1.0")
    st.caption("Desenvolvido por MB Technological Solutions®")


if __name__ == "__main__":
    main()
