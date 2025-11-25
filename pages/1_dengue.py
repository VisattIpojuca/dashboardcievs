import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Dengue - Análise",
    page_icon="🦟",
    layout="wide"
)

st.title("🦟 Análise de Casos de Dengue")

# Função para gerar dados de exemplo
@st.cache_data
def gerar_dados_exemplo():
    """Gera dados de exemplo para demonstração"""
    np.random.seed(42)

    # Gerar datas
    data_inicio = datetime(2023, 1, 1)
    datas = [data_inicio + timedelta(days=x) for x in range(365)]

    # Gerar casos com sazonalidade
    casos = []
    for i, data in enumerate(datas):
        # Mais casos no verão (meses 1-3 e 12)
        mes = data.month
        if mes in [1, 2, 3, 12]:
            base = 50
        elif mes in [4, 5, 11]:
            base = 30
        else:
            base = 10

        # Adicionar variação aleatória
        caso = max(0, int(base + np.random.normal(0, 10)))
        casos.append(caso)

    df = pd.DataFrame({
        'data': datas,
        'casos': casos,
        'mes': [d.month for d in datas],
        'ano': [d.year for d in datas]
    })

    # Adicionar dados por região
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    df_regioes = pd.DataFrame({
        'regiao': regioes,
        'casos': np.random.randint(100, 500, len(regioes)),
        'populacao': np.random.randint(50000, 150000, len(regioes))
    })
    df_regioes['incidencia'] = (df_regioes['casos'] / df_regioes['populacao'] * 100000).round(2)

    return df, df_regioes

# Carregar dados
df_temporal, df_regioes = gerar_dados_exemplo()

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro de período
periodo = st.sidebar.selectbox(
    "Período de análise",
    ["Último mês", "Últimos 3 meses", "Últimos 6 meses", "Ano completo"]
)

# Mapear período para dias
periodo_dias = {
    "Último mês": 30,
    "Últimos 3 meses": 90,
    "Últimos 6 meses": 180,
    "Ano completo": 365
}

dias = periodo_dias[periodo]
df_filtrado = df_temporal.tail(dias)

# Métricas principais
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total_casos = df_filtrado['casos'].sum()
media_diaria = df_filtrado['casos'].mean()
max_casos = df_filtrado['casos'].max()
tendencia = "↑" if df_filtrado['casos'].tail(7).mean() > df_filtrado['casos'].head(7).mean() else "↓"

with col1:
    st.metric("Total de Casos", f"{total_casos:,}", delta=f"{tendencia}")

with col2:
    st.metric("Média Diária", f"{media_diaria:.1f}")

with col3:
    st.metric("Pico de Casos", f"{max_casos}")

with col4:
    if len(df_filtrado) >= 60:
        variacao = ((df_filtrado['casos'].tail(30).sum() / df_filtrado['casos'].head(30).sum() - 1) * 100)
    else:
        variacao = 0
    st.metric("Variação Mensal", f"{variacao:.1f}%", delta=f"{variacao:.1f}%")

# Gráfico temporal
st.header("📈 Evolução Temporal")

fig_temporal = px.line(
    df_filtrado,
    x='data',
    y='casos',
    title='Casos de Dengue ao Longo do Tempo',
    labels={'data': 'Data', 'casos': 'Número de Casos'}
)

fig_temporal.update_traces(line_color='#FF6B6B', line_width=2)
fig_temporal.update_layout(
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig_temporal, use_container_width=True)

# Análise por região
st.header("🗺️ Análise por Região")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras - casos por região
    fig_barras = px.bar(
        df_regioes.sort_values('casos', ascending=False),
        x='regiao',
        y='casos',
        title='Casos por Região',
        labels={'regiao': 'Região', 'casos': 'Número de Casos'},
        color='casos',
        color_continuous_scale='Reds'
    )
    fig_barras.update_layout(showlegend=False)
    st.plotly_chart(fig_barras, use_container_width=True)

with col2:
    # Gráfico de pizza - distribuição percentual
    fig_pizza = px.pie(
        df_regioes,
        values='casos',
        names='regiao',
        title='Distribuição Percentual de Casos'
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# Tabela de incidência
st.header("📋 Taxa de Incidência por Região")
st.markdown("*Taxa de incidência por 100.000 habitantes*")

df_regioes_display = df_regioes.sort_values('incidencia', ascending=False)
df_regioes_display = df_regioes_display.rename(columns={
    'regiao': 'Região',
    'casos': 'Casos',
    'populacao': 'População',
    'incidencia': 'Incidência (por 100k hab.)'
})

st.dataframe(
    df_regioes_display,
    use_container_width=True,
    hide_index=True
)

# Análise mensal
st.header("📅 Análise Mensal")

df_mensal = df_temporal.groupby('mes')['casos'].sum().reset_index()
meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
df_mensal['mes_nome'] = df_mensal['mes'].apply(lambda x: meses_nomes[x-1])

fig_mensal = px.bar(
    df_mensal,
    x='mes_nome',
    y='casos',
    title='Distribuição de Casos por Mês',
    labels={'mes_nome': 'Mês', 'casos': 'Total de Casos'},
    color='casos',
    color_continuous_scale='YlOrRd'
)

st.plotly_chart(fig_mensal, use_container_width=True)

# Informações adicionais
with st.expander("ℹ️ Informações sobre os dados"):
    st.markdown("""
    ### Sobre os dados

    - **Fonte:** Dados de exemplo para demonstração
    - **Período:** 2023
    - **Atualização:** Dados simulados

    ### Metodologia

    - **Taxa de Incidência:** Calculada por 100.000 habitantes
    - **Tendência:** Baseada na comparação entre primeira e última semana do período

    ### Observações

    - Os dados apresentados são fictícios e servem apenas para demonstração
    - Em produção, conecte a fontes de dados reais (CSV, banco de dados, API)
    """)

# Footer
st.markdown("---")
st.markdown("*Painel de Monitoramento de Dengue - Versão 1.0*")
