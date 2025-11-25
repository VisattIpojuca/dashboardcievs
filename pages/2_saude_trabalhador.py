import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Saúde do Trabalhador",
    page_icon="👷",
    layout="wide"
)

st.title("👷 Saúde do Trabalhador - Análise de Acidentes")

# Função para gerar dados de exemplo
@st.cache_data
def gerar_dados_acidentes():
    """Gera dados de exemplo de acidentes de trabalho"""
    np.random.seed(42)

    setores = ['Construção Civil', 'Indústria', 'Comércio', 'Serviços', 'Agricultura']
    tipos = ['Queda', 'Corte', 'Queimadura', 'Esmagamento', 'Outros']
    severidade = ['Leve', 'Moderado', 'Grave']

    data_inicio = datetime(2023, 1, 1)
    datas = [data_inicio + timedelta(days=x * 7) for x in range(52)]  # Semanal

    acidentes_semana = []
    tipos_aleatorios = []
    severidades = []
    setores_aleatorios = []

    for data in datas:
        acidentes = max(5, int(np.random.normal(20, 5)))
        acidentes_semana.append(acidentes)
        tipos_aleatorios.append(np.random.choice(tipos))
        severidades.append(np.random.choice(severidade))
        setores_aleatorios.append(np.random.choice(setores))

    df_temporal = pd.DataFrame({
        'data': datas,
        'acidentes': acidentes_semana,
        'tipo': tipos_aleatorios,
        'severidade': severidades,
        'setor': setores_aleatorios
    })

    df_setores = pd.DataFrame({
        'setor': setores,
        'acidentes': np.random.randint(50, 200, len(setores)),
        'trabalhadores': np.random.randint(1000, 5000, len(setores))
    })
    df_setores['taxa'] = (df_setores['acidentes'] / df_setores['trabalhadores'] * 1000).round(2)

    df_tipos = pd.DataFrame({
        'tipo': tipos,
        'quantidade': np.random.randint(30, 150, len(tipos))
    })

    return df_temporal, df_setores, df_tipos


# Carregar dados
df_temporal, df_setores, df_tipos = gerar_dados_acidentes()

# Sidebar — NOVOS FILTROS
st.sidebar.header("Filtros")

# FILTRO POR DATA
min_date = df_temporal['data'].min()
max_date = df_temporal['data'].max()

intervalo_data = st.sidebar.date_input(
    "Selecione o período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# FILTRO POR ANO
df_temporal['ano'] = df_temporal['data'].dt.year
anos = st.sidebar.multiselect(
    "Ano",
    options=sorted(df_temporal['ano'].unique()),
    default=sorted(df_temporal['ano'].unique())
)

# FILTRO POR MÊS
df_temporal['mes'] = df_temporal['data'].dt.month
meses_nomes = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
df_temporal['mes_nome'] = df_temporal['mes'].map(meses_nomes)

meses = st.sidebar.multiselect(
    "Mês",
    options=meses_nomes.values(),
    default=list(meses_nomes.values())
)

# FILTRO POR SETOR
setor_selecionado = st.sidebar.multiselect(
    "Setor",
    options=df_setores['setor'].tolist(),
    default=df_setores['setor'].tolist()
)

# FILTRO POR TIPO DE ACIDENTE
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de acidente",
    options=df_tipos['tipo'].tolist(),
    default=df_tipos['tipo'].tolist()
)

# FILTRO POR SEVERIDADE (adicionado)
severidade_sel = st.sidebar.multiselect(
    "Severidade",
    options=df_temporal['severidade'].unique(),
    default=df_temporal['severidade'].unique()
)

# FILTRO POR INTERVALO DE ACIDENTES NOS SETORES
min_ac = int(df_setores['acidentes'].min())
max_ac = int(df_setores['acidentes'].max())

intervalo_acidentes = st.sidebar.slider(
    "Acidentes por setor (intervalo)",
    min_value=min_ac,
    max_value=max_ac,
    value=(min_ac, max_ac)
)

# Aplicando filtros ao df temporal
df_filt = df_temporal.copy()

# Filtros aplicados
df_filt = df_filt[
    (df_filt['data'] >= pd.to_datetime(intervalo_data[0])) &
    (df_filt['data'] <= pd.to_datetime(intervalo_data[1])) &
    (df_filt['ano'].isin(anos)) &
    (df_filt['mes_nome'].isin(meses)) &
    (df_filt['severidade'].isin(severidade_sel)) &
    (df_filt['tipo'].isin(tipos_selecionados)) &
    (df_filt['setor'].isin(setor_selecionado))
]

# Filtro no df_setores
df_setores_filtrado = df_setores[
    (df_setores['setor'].isin(setor_selecionado)) &
    (df_setores['acidentes'].between(intervalo_acidentes[0], intervalo_acidentes[1]))
]

# ===============================
# Indicadores principais
# ===============================
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total_acidentes = df_filt['acidentes'].sum()
media_semanal = df_filt['acidentes'].mean()
setor_maior = df_setores_filtrado.loc[df_setores_filtrado['acidentes'].idxmax(), 'setor'] \
    if not df_setores_filtrado.empty else "—"
taxa_media = df_setores_filtrado['taxa'].mean() if not df_setores_filtrado.empty else 0

col1.metric("Total de Acidentes", f"{total_acidentes:,}")
col2.metric("Média Semanal", f"{media_semanal:.1f}")
col3.metric("Setor com Mais Acidentes", setor_maior)
col4.metric("Taxa Média", f"{taxa_media:.2f}‰")

# ===============================
# Gráfico temporal
# ===============================
st.header("📈 Evolução de Acidentes")

fig_temporal = go.Figure()

fig_temporal.add_trace(go.Scatter(
    x=df_filt['data'],
    y=df_filt['acidentes'],
    mode='lines+markers',
    name='Acidentes',
    line=dict(color='#FF6B6B', width=2),
    marker=dict(size=6)
))

df_filt['media_movel'] = df_filt['acidentes'].rolling(window=4).mean()

fig_temporal.add_trace(go.Scatter(
    x=df_filt['data'],
    y=df_filt['media_movel'],
    mode='lines',
    name='Média Móvel (4 semanas)',
    line=dict(color='#4ECDC4', width=2, dash='dash')
))

fig_temporal.update_layout(
    title='Acidentes de Trabalho ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Número de Acidentes',
    hovermode='x unified'
)

st.plotly_chart(fig_temporal, use_container_width=True)

# ===============================
# Análise por setor
# ===============================
st.header("🏭 Análise por Setor")

col1, col2 = st.columns(2)

with col1:
    fig_setores = px.bar(
        df_setores_filtrado.sort_values('acidentes', ascending=True),
        y='setor',
        x='acidentes',
        orientation='h',
        title='Acidentes por Setor'
    )
    st.plotly_chart(fig_setores, use_container_width=True)

with col2:
    fig_taxa = px.bar(
        df_setores_filtrado.sort_values('taxa', ascending=True),
        y='setor',
        x='taxa',
        orientation='h',
        title='Taxa de Acidentes por 1000 Trabalhadores'
    )
    st.plotly_chart(fig_taxa, use_container_width=True)

# ===============================
# Tipos de Acidentes
# ===============================
st.header("🔍 Tipos de Acidentes")

fig_tipos = px.bar(
    df_tipos[df_tipos['tipo'].isin(tipos_selecionados)],
    x='tipo',
    y='quantidade',
    title='Distribuição por Tipo de Acidente'
)

st.plotly_chart(fig_tipos, use_container_width=True)

# ===============================
# Tabela detalhada por setor
# ===============================
st.header("📋 Detalhamento por Setor")

df_setores_display = df_setores_filtrado.rename(columns={
    'setor': 'Setor',
    'acidentes': 'Acidentes',
    'trabalhadores': 'Trabalhadores',
    'taxa': 'Taxa (por 1000)'
})

st.dataframe(df_setores_display, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Painel de Saúde do Trabalhador - Versão 1.1*")
