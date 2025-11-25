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

# ===============================
#   FUNÇÃO PARA GERAR DADOS FAKE
#   (Substitua futuramente pela sua planilha real)
# ===============================
@st.cache_data
def gerar_dados_acidentes():
    np.random.seed(42)

    setores = ['Construção Civil', 'Indústria', 'Comércio', 'Serviços', 'Agricultura']
    tipos = ['Queda', 'Corte', 'Queimadura', 'Esmagamento', 'Outros']

    data_inicio = datetime(2023, 1, 1)
    datas = [data_inicio + timedelta(days=x*7) for x in range(52)]

    acidentes_semana = [max(5, int(np.random.normal(20, 5))) for _ in datas]

    df_temporal = pd.DataFrame({
        'DATA': datas,
        'ACIDENTES': acidentes_semana
    })

    df_setores = pd.DataFrame({
        'SETOR': setores,
        'ACIDENTES': np.random.randint(50, 200, len(setores)),
        'TRABALHADORES': np.random.randint(1000, 5000, len(setores))
    })
    df_setores['TAXA'] = (df_setores['ACIDENTES'] / df_setores['TRABALHADORES'] * 1000).round(2)

    df_tipos = pd.DataFrame({
        'TIPO': tipos,
        'QUANTIDADE': np.random.randint(30, 150, len(tipos))
    })

    # 🔥 FINGINDO TODAS AS COLUNAS PARA OS FILTROS NOVOS
    df_temporal['SEMANA_EPIDEMIOLOGICA'] = df_temporal['DATA'].dt.isocalendar().week
    df_temporal['IDADE'] = np.random.choice(range(18, 70), len(df_temporal))
    df_temporal['SEXO'] = np.random.choice(['Masculino', 'Feminino'], len(df_temporal))
    df_temporal['RACA_COR'] = np.random.choice(['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena'], len(df_temporal))
    df_temporal['ESCOLARIDADE'] = np.random.choice(
        ['Fundamental', 'Médio', 'Superior', 'Pós-Graduação'], len(df_temporal)
    )
    df_temporal['OCUPACAO'] = np.random.choice(
        ['Operador', 'Servente', 'Técnico', 'Supervisor', 'Autônomo'], len(df_temporal)
    )
    df_temporal['SITUACAO_MERCADO_TRABALHO'] = np.random.choice(
        ['Empregado', 'Desempregado', 'Autônomo', 'Estagiário'], len(df_temporal)
    )
    df_temporal['BAIRRO_OCORRENCIA'] = np.random.choice(
        ['Ipojuca Sede', 'Nossa Senhora do Ó', 'Camela', 'Porto de Galinhas'], len(df_temporal)
    )
    df_temporal['EVOLUCAO_DO_CASO'] = np.random.choice(
        ['Alta', 'Óbito', 'Encerrado', 'Afastamento'], len(df_temporal)
    )

    return df_temporal, df_setores, df_tipos


# Carregamento dos dados
df, df_setores, df_tipos = gerar_dados_acidentes()

# =====================================================
#   SISTEMA AUTOMÁTICO DE FILTROS NA SIDEBAR
# =====================================================

st.sidebar.header("Filtros")

df_filtrado = df.copy()

def filtrar(col, label=None, ordenar=False):
    if col in df_filtrado.columns:
        opcoes = df_filtrado[col].dropna().unique().tolist()
        if ordenar:
            opcoes = sorted(opcoes)
        selecao = st.sidebar.multiselect(label or col, opcoes)
        if selecao:
            return df_filtrado[df_filtrado[col].isin(selecao)]
    return df_filtrado

# 🔥 Filtros solicitados
df_filtrado = filtrar("SEMANA_EPIDEMIOLOGICA", "Semana Epidemiológica", ordenar=True)
df_filtrado = filtrar("IDADE", "Idade", ordenar=True)
df_filtrado = filtrar("SEXO", "Sexo")
df_filtrado = filtrar("RACA_COR", "Raça/Cor", ordenar=True)
df_filtrado = filtrar("ESCOLARIDADE", "Escolaridade", ordenar=True)
df_filtrado = filtrar("OCUPACAO", "Ocupação", ordenar=True)
df_filtrado = filtrar("SITUACAO_MERCADO_TRABALHO", "Situação no Mercado de Trabalho", ordenar=True)
df_filtrado = filtrar("BAIRRO_OCORRENCIA", "Bairro de Ocorrência", ordenar=True)
df_filtrado = filtrar("EVOLUCAO_DO_CASO", "Evolução do Caso", ordenar=True)

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()


# =====================================================
#   INDICADORES PRINCIPAIS
# =====================================================

st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total_acidentes = df_filtrado['ACIDENTES'].sum()
media_semanal = df_filtrado['ACIDENTES'].mean()
taxa_media = df_setores['TAXA'].mean()
setor_maior = df_setores.loc[df_setores['ACIDENTES'].idxmax(), 'SETOR']

col1.metric("Total de Acidentes", f"{total_acidentes:,}")
col2.metric("Média Semanal", f"{media_semanal:.1f}")
col3.metric("Setor com Mais Acidentes", setor_maior)
col4.metric("Taxa Média", f"{taxa_media:.2f}‰")


# =====================================================
#   GRÁFICO TEMPORAL
# =====================================================

st.header("📈 Evolução de Acidentes")

fig_temporal = go.Figure()

fig_temporal.add_trace(go.Scatter(
    x=df_filtrado['DATA'],
    y=df_filtrado['ACIDENTES'],
    mode='lines+markers',
    name='Acidentes',
    line=dict(color='#FF6B6B', width=2),
    marker=dict(size=6)
))

df_filtrado['MEDIA_MOVEL'] = df_filtrado['ACIDENTES'].rolling(window=4).mean()

fig_temporal.add_trace(go.Scatter(
    x=df_filtrado['DATA'],
    y=df_filtrado['MEDIA_MOVEL'],
    mode='lines',
    name='Média Móvel (4 semanas)',
    line=dict(color='#4ECDC4', width=2, dash='dash')
))

fig_temporal.update_layout(
    title='Acidentes de Trabalho ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Número de Acidentes',
    hovermode='x unified',
)

st.plotly_chart(fig_temporal, use_container_width=True)


# =====================================================
#   ANÁLISE POR SETOR
# =====================================================

st.header("🏭 Análise por Setor")

df_setores_filtrado = df_setores.copy()

c1, c2 = st.columns(2)

with c1:
    fig_setores = px.bar(
        df_setores_filtrado.sort_values('ACIDENTES'),
        y='SETOR', x='ACIDENTES',
        title='Acidentes por Setor',
        orientation='h'
    )
    st.plotly_chart(fig_setores, use_container_width=True)

with c2:
    fig_taxa = px.bar(
        df_setores_filtrado.sort_values('TAXA'),
        y='SETOR', x='TAXA',
        title='Taxa por 1.000 Trabalhadores',
        orientation='h'
    )
    st.plotly_chart(fig_taxa, use_container_width=True)


# =====================================================
#   TIPOS DE ACIDENTE
# =====================================================

st.header("🔍 Tipos de Acidentes")

c3, c4 = st.columns([2, 1])

with c3:
    fig_tipos = px.bar(
        df_tipos.sort_values('QUANTIDADE', ascending=False),
        x='TIPO', y='QUANTIDADE',
        title='Distribuição por Tipo de Acidente'
    )
    st.plotly_chart(fig_tipos, use_container_width=True)

with c4:
    df_tipos_display = df_tipos.copy()
    df_tipos_display['%'] = (
        df_tipos_display['QUANTIDADE'] / df_tipos_display['QUANTIDADE'].sum() * 100
    ).round(1)
    st.dataframe(df_tipos_display, hide_index=True)


# =====================================================
#   DETALHAMENTO POR SETOR
# =====================================================

st.header("📋 Detalhamento por Setor")

df_det = df_setores_filtrado.rename(columns={
    'SETOR': 'Setor',
    'ACIDENTES': 'Acidentes',
    'TRABALHADORES': 'Trabalhadores',
    'TAXA': 'Taxa (por 1000)'
})

st.dataframe(df_det, hide_index=True, use_container_width=True)

st.markdown("---")
st.caption("Painel de Saúde do Trabalhador - Versão 1.0")
