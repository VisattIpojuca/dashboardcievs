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
# CSS — PALETA INSTITUCIONAL FIXA (NÃO MUDA NO DARK MODE)
# =======================================================

st.markdown("""
<style>

:root {
    --azul-principal: #004A8D;
    --azul-secundario: #0073CF;
    --verde-ipojuca: #009D4A;
    --amarelo-ipojuca: #FFC20E;
    --cinza-claro: #F2F2F2;
    --branco: #FFFFFF;
}

/* Texto sempre preto */
html, body, * {
    color: #000 !important;
}

/* Títulos amarelo */
h1, h2, h3, h4 {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 800 !important;
}

/* Parágrafos justificados */
p, li {
    text-align: justify !important;
    color: #000 !important;
}

/* Fundo geral */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--azul-principal) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] a {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 600;
}

/* Métricas */
.stMetric {
    background-color: var(--amarelo-ipojuca) !important;
    padding: 18px;
    border-radius: 10px;
    border-left: 6px solid var(--azul-secundario);
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}

/* Botões */
button, .stButton button {
    color: #000 !important;
    background-color: var(--cinza-claro) !important;
}

</style>
""", unsafe_allow_html=True)

# =======================================================
# PÁGINA — TÍTULO
# =======================================================
st.title("🦟 Dashboard Vigilância das Arboviroses (Dengue)")
st.caption("Fonte: Gerência de Promoção, Prevenção e Vigilância Epidemiológica 📊🗺️")


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
    '1 a 4 anos','5 a 9 anos','10 a 14 anos','15 a 19 anos',
    '20 a 39 anos','40 a 59 anos','60 anos ou mais','IGNORADO'
]

MAPEAMENTO_FAIXA_ETARIA = {
    '0 a 4': '1
