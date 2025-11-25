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

    # Setores
    setores = ['Construção Civil', 'Indústria', 'Comércio', 'Serviços', 'Agricultura']

    # Tipos de acidente
    tipos = ['Queda', 'Corte', 'Queimadura', 'Esmagamento', 'Outros']

    # Gerar dados temporais
    data_inicio = datetime(2023, 1, 1)
    datas = [data_inicio + timedelta(days=x*7) for x in range(52)]  # Semanal

    acidentes_semana = []
    for data in datas:
        acidentes = max(5, int(np.random.normal(20, 5)))
        acidentes_semana.append(acidentes)

    df_temporal = pd.DataFrame({
        'data': datas,
        'acidentes': acidentes_semana
    })

    # Dados por setor
    df_setores = pd.DataFrame({
        'setor': setores,
        'acidentes': np.random.randint(50, 200, len(setores)),
        'trabalhadores': np.random.randint(1000, 5000, len(setores))
    })
    df_setores['taxa'] = (df_setores['acidentes'] / df_setores['trabalhadores'] * 1000).round(2)

    # Dados por tipo
    df_tipos = pd.DataFrame({
        'tipo': tipos,
        'quantidade': np.random.randint(30, 150, len(tipos))
    })

    return df_temporal, df_setores, df_tipos

# Carregar dados
df_temporal, df_setores, df_tipos = gerar_dados_acidentes()

# Sidebar
st.sidebar.header("Filtros")

setor_selecionado = st.sidebar.multiselect(
    "Selecione os setores",
    options=df_setores['setor'].tolist(),
    default=df_setores['setor'].tolist()
)

# Métricas principais
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total_acidentes = df_temporal['acidentes'].sum()
media_semanal = df_temporal['acidentes'].mean()
setor_maior = df_setores.loc[df_setores['acidentes'].idxmax(), 'setor']
taxa_media = df_setores['taxa'].mean()

with col1:
    st.metric("Total de Acidentes", f"{total_acidentes:,}")

with col2:
    st.metric("Média Semanal", f"{media_semanal:.1f}")

with col3:
    st.metric("Setor com Mais Acidentes", setor_maior)

with col4:
    st.metric("Taxa Média", f"{taxa_media:.2f}‰")

# Gráfico temporal
st.header("📈 Evolução de Acidentes")

fig_temporal = go.Figure()

fig_temporal.add_trace(go.Scatter(
    x=df_temporal['data'],
    y=df_temporal['acidentes'],
    mode='lines+markers',
    name='Acidentes',
    line=dict(color='#FF6B6B', width=2),
    marker=dict(size=6)
))

# Adicionar média móvel
df_temporal['media_movel'] = df_temporal['acidentes'].rolling(window=4).mean()

fig_temporal.add_trace(go.Scatter(
    x=df_temporal['data'],
    y=df_temporal['media_movel'],
    mode='lines',
    name='Média Móvel (4 semanas)',
    line=dict(color='#4ECDC4', width=2, dash='dash')
))

fig_temporal.update_layout(
    title='Acidentes de Trabalho ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Número de Acidentes',
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig_temporal, use_container_width=True)

# Análise por setor
st.header("🏭 Análise por Setor")

# Filtrar setores selecionados
df_setores_filtrado = df_setores[df_setores['setor'].isin(setor_selecionado)]

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras - acidentes por setor
    fig_setores = px.bar(
        df_setores_filtrado.sort_values('acidentes', ascending=True),
        y='setor',
        x='acidentes',
        orientation='h',
        title='Acidentes por Setor',
        labels={'setor': 'Setor', 'acidentes': 'Número de Acidentes'},
        color='acidentes',
        color_continuous_scale='Reds'
    )
    fig_setores.update_layout(showlegend=False)
    st.plotly_chart(fig_setores, use_container_width=True)

with col2:
    # Gráfico de taxa por setor
    fig_taxa = px.bar(
        df_setores_filtrado.sort_values('taxa', ascending=True),
        y='setor',
        x='taxa',
        orientation='h',
        title='Taxa de Acidentes por 1000 Trabalhadores',
        labels={'setor': 'Setor', 'taxa': 'Taxa (por 1000)'},
        color='taxa',
        color_continuous_scale='Oranges'
    )
    fig_taxa.update_layout(showlegend=False)
    st.plotly_chart(fig_taxa, use_container_width=True)

# Análise por tipo de acidente
st.header("🔍 Tipos de Acidentes")

col1, col2 = st.columns([2, 1])

with col1:
    fig_tipos = px.bar(
        df_tipos.sort_values('quantidade', ascending=False),
        x='tipo',
        y='quantidade',
        title='Distribuição por Tipo de Acidente',
        labels={'tipo': 'Tipo de Acidente', 'quantidade': 'Quantidade'},
        color='quantidade',
        color_continuous_scale='Blues'
    )
    fig_tipos.update_layout(showlegend=False)
    st.plotly_chart(fig_tipos, use_container_width=True)

with col2:
    # Tabela de tipos
    st.markdown("### Resumo")
    df_tipos_display = df_tipos.sort_values('quantidade', ascending=False)
    df_tipos_display['percentual'] = (df_tipos_display['quantidade'] / df_tipos_display['quantidade'].sum() * 100).round(1)
    df_tipos_display = df_tipos_display.rename(columns={
        'tipo': 'Tipo',
        'quantidade': 'Qtd',
        'percentual': '%'
    })
    st.dataframe(df_tipos_display, use_container_width=True, hide_index=True)

# Tabela detalhada por setor
st.header("📋 Detalhamento por Setor")

df_setores_display = df_setores_filtrado.sort_values('acidentes', ascending=False)
df_setores_display = df_setores_display.rename(columns={
    'setor': 'Setor',
    'acidentes': 'Acidentes',
    'trabalhadores': 'Trabalhadores',
    'taxa': 'Taxa (por 1000)'
})

st.dataframe(
    df_setores_display,
    use_container_width=True,
    hide_index=True
)

# Informações adicionais
with st.expander("ℹ️ Informações sobre os dados"):
    st.markdown("""
    ### Sobre os dados

    - **Fonte:** Dados de exemplo para demonstração
    - **Período:** 2023 (dados semanais)
    - **Atualização:** Dados simulados

    ### Metodologia

    - **Taxa de Acidentes:** Calculada por 1.000 trabalhadores
    - **Média Móvel:** Calculada com janela de 4 semanas

    ### Classificação de Acidentes

    - **Queda:** Quedas de altura ou mesmo nível
    - **Corte:** Ferimentos por objetos cortantes
    - **Queimadura:** Queimaduras térmicas, químicas ou elétricas
    - **Esmagamento:** Acidentes com prensagem ou esmagamento
    - **Outros:** Demais tipos de acidentes

    ### Observações

    - Os dados apresentados são fictícios e servem apenas para demonstração
    - Em produção, conecte a fontes de dados reais (SINAN, CAT, etc.)
    """)

# Footer
st.markdown("---")
st.markdown("*Painel de Saúde do Trabalhador - Versão 1.0*")
