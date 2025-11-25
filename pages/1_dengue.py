import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import unicodedata

# =======================================================
# Página: 1 — DENGUE (compatível com o multipage do Streamlit)
# =======================================================

st.title("🦟 Dashboard Vigilância das Arboviroses (Dengue)")
st.caption("Fonte: Gerência de Promoção, Prevenção e Vigilância Epidemiológica 📊🗺️")

# =======================================================
# MAPEAMENTOS, PADRONIZAÇÃO E CONFIGURAÇÕES
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
    '0 a 4': '1 a 4 anos','1 a 4': '1 a 4 anos','5 a 9': '5 a 9 anos',
    '10 a 14': '10 a 14 anos','15 a 19': '15 a 19 anos',
    '20 a 29': '20 a 39 anos','30 a 39': '20 a 39 anos',
    '40 a 49': '40 a 59 anos','50 a 59': '40 a 59 anos',
    '60 a 69': '60 anos ou mais','70 a 79': '60 anos ou mais',
    '80 ou mais': '60 anos ou mais','IGNORADO': 'IGNORADO'
}

def limpar_nome_coluna(col):
    c = unicodedata.normalize('NFKD', col).encode('ascii','ignore').decode()
    return c.strip().upper().replace(" ","_").replace("-","_").replace("/","_")


# =======================================================
# CARREGAMENTO DO DATASET
# =======================================================

@st.cache_data
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1bdHetdGEXLgXv7A2aGvOaItKxiAuyg0Ip0UER1BjjOg/export?format=csv"
    try:
        df = pd.read_csv(url)
    except Exception:
        st.error("❌ Erro ao carregar os dados da planilha do Google Sheets.")
        st.stop()

    df.columns = [limpar_nome_coluna(c) for c in df.columns]

    rename_dict = {orig:dest for orig,dest in FINAL_RENAME_MAP.items() if orig in df.columns}
    df.rename(columns=rename_dict, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]

    if 'FAIXA_ETARIA' in df.columns:
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].astype(str).str.strip()
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].replace(MAPEAMENTO_FAIXA_ETARIA)
        df['FAIXA_ETARIA'] = df['FAIXA_ETARIA'].fillna("IGNORADO")

    for col in ['DATA_NOTIFICACAO','DATA_SINTOMAS']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()


# =======================================================
# FILTROS — SIDEBAR
# =======================================================

st.sidebar.header("🔎 Filtros")
df_filtrado = df.copy()

if 'CLASSIFICACAO_FINAL' in df.columns:
    f = st.sidebar.multiselect("Classificação Final", df['CLASSIFICACAO_FINAL'].dropna().unique())
    if f: df_filtrado = df_filtrado[df_filtrado['CLASSIFICACAO_FINAL'].isin(f)]

if 'SEMANA_EPIDEMIOLOGICA' in df.columns:
    semanas = st.sidebar.multiselect("Semana Epidemiológica", sorted(df['SEMANA_EPIDEMIOLOGICA'].dropna().unique()))
    if semanas: df_filtrado = df_filtrado[df_filtrado['SEMANA_EPIDEMIOLOGICA'].isin(semanas)]

if 'SEXO' in df.columns:
    sex = st.sidebar.multiselect("Sexo", df['SEXO'].dropna().unique())
    if sex: df_filtrado = df_filtrado[df_filtrado['SEXO'].isin(sex)]

if 'FAIXA_ETARIA' in df.columns:
    faixas = st.sidebar.multiselect("Faixa Etária", ORDEM_FAIXA_ETARIA)
    if faixas: df_filtrado = df_filtrado[df_filtrado['FAIXA_ETARIA'].isin(faixas)]

if 'EVOLUCAO' in df.columns:
    evo = st.sidebar.multiselect("Evolução do Caso", df['EVOLUCAO'].dropna().unique())
    if evo: df_filtrado = df_filtrado[df_filtrado['EVOLUCAO'].isin(evo)]

if 'ESCOLARIDADE' in df.columns:
    esc = st.sidebar.multiselect("Escolaridade", df['ESCOLARIDADE'].dropna().unique())
    if esc: df_filtrado = df_filtrado[df_filtrado['ESCOLARIDADE'].isin(esc)]

if 'BAIRRO' in df.columns:
    bai = st.sidebar.multiselect("Bairro", sorted(df['BAIRRO'].dropna().unique()))
    if bai: df_filtrado = df_filtrado[df_filtrado['BAIRRO'].isin(bai)]


if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()


# =======================================================
# CARDS / INDICADORES
# =======================================================

st.header("📊 Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)

total = len(df_filtrado)
col1.metric("Notificações no período", total)

if 'CLASSIFICACAO_FINAL' in df_filtrado.columns:
    classif = df_filtrado['CLASSIFICACAO_FINAL'].astype(str).str.upper().str.strip()
    confirmados = classif.isin(["DENGUE","DENGUE COM SINAIS DE ALARME"]).sum()
    descartados = (classif == "DESCARTADO").sum()

    col2.metric("Confirmados", confirmados)
    col3.metric("Descartados", descartados)

if 'EVOLUCAO' in df_filtrado.columns:
    obitos = df_filtrado['EVOLUCAO'].astype(str).str.upper().str.contains("ÓBITO").sum()
    let = (obitos/confirmados)*100 if confirmados else 0
    col4.metric("Letalidade (%)", f"{let:.2f}% ({obitos} óbitos)")


# =======================================================
# GRÁFICOS
# =======================================================

st.subheader("📈 Análise Temporal e Territorial")
colA, colB = st.columns(2)

if 'SEMANA_EPIDEMIOLOGICA' in df_filtrado.columns:
    semanal = df_filtrado.groupby("SEMANA_EPIDEMIOLOGICA").size().reset_index(name="Casos")
    fig = px.line(semanal, x="SEMANA_EPIDEMIOLOGICA", y="Casos", markers=True,
                  title="Casos por Semana Epidemiológica")
    colA.plotly_chart(fig, use_container_width=True)

if 'DISTRITO' in df_filtrado.columns:
    d = df_filtrado['DISTRITO'].value_counts().reset_index()
    d.columns = ['Distrito','Casos']
    fig = px.bar(d, x="Distrito", y="Casos", title="Distribuição de Casos por Distrito")
    colB.plotly_chart(fig, use_container_width=True)

# — BAIRROS
st.subheader("🏘️ Casos por Bairro")
if 'BAIRRO' in df_filtrado.columns:
    b = df_filtrado['BAIRRO'].value_counts().reset_index()
    b.columns = ['Bairro','Casos']
    fig = px.bar(b.head(15), x="Bairro", y="Casos", title="Top 15 Bairros")
    st.plotly_chart(fig, use_container_width=True)

# — SOCIODEMOGRÁFICO
st.subheader("🎓 Perfil Social")
if 'RACA_COR' in df_filtrado.columns and 'ESCOLARIDADE' in df_filtrado.columns:
    cruz = df_filtrado.groupby(['RACA_COR','ESCOLARIDADE']).size().reset_index(name='Casos')
    fig = px.bar(cruz, x="RACA_COR", y="Casos", color="ESCOLARIDADE",
                 barmode="group", title="Casos por Raça/Cor e Escolaridade")
    st.plotly_chart(fig, use_container_width=True)

# — SINTOMAS
st.subheader("🩺 Sintomas e Comorbidades")
sintomas_e_comorbidades = [
    "FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA",
    "DOR_COSTAS","CONJUNTVITE","ARTRITE","ARTRALGIA","PETEQUIAS",
    "LEUCOPENIA","LACO","DOR_RETRO","DIABETES","HEMATOLOGICAS",
    "HEPATOPATIAS","RENAL","HIPERTENSAO","ACIDO_PEPT","AUTO_IMUNE"
]

dados = []
for s in sintomas_e_comorbidades:
    colname = limpar_nome_coluna(s)
    if colname in df_filtrado.columns:
        ct = (df_filtrado[colname].astype(str).str.upper().str.strip() == "SIM").sum()
        if ct > 0:
            dados.append({"Item": s.replace("_"," ").capitalize(), "Casos": ct})

if dados:
    df_s = pd.DataFrame(dados)
    fig = px.bar(df_s.sort_values("Casos"), x="Casos", y="Item",
                 orientation='h', title="Frequência de Sintomas e Comorbidades")
    st.plotly_chart(fig, use_container_width=True)

# — FAIXA ETÁRIA X SEXO
st.subheader("👥 Perfil Demográfico")
if 'FAIXA_ETARIA' in df_filtrado.columns and 'SEXO' in df_filtrado.columns:
    ordem_plot = [f for f in ORDEM_FAIXA_ETARIA if f in df_filtrado['FAIXA_ETARIA'].unique()]
    fig = px.histogram(df_filtrado, x="FAIXA_ETARIA", color="SEXO",
                       barmode="group", title="Casos por Faixa Etária e Sexo")
    fig.update_xaxes(categoryorder="array", categoryarray=ordem_plot)
    st.plotly_chart(fig, use_container_width=True)

# =======================================================
# DOWNLOAD
# =======================================================

st.download_button(
    "📥 Baixar dados filtrados (CSV)",
    df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="dados_filtrados_dengue.csv",
    mime="text/csv"
)

st.caption("Desenvolvido pelo CIEVS Ipojuca.")
