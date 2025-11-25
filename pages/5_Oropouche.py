# pages/1_oropouche.py
"""
Dashboard Oropouche — Página Streamlit
- Usa Data da Notificação para séries mensais
- Filtros: Localidade, Classificação, Semana Epidemiológica, Sexo, Raça/Cor
- Tabela final oculta: MES, DATA_DE_NASCIMENTO, NOME, RUA, TELEFONE, etc.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Oropouche - Dashboard",
    page_icon="🦟",
    layout="wide"
)

st.title("🦟 Dashboard de Oropouche - Vigilância em Saúde")
st.markdown("Monitoramento por localidade, classificação e período. Dados sensíveis ocultos automaticamente.")

# ---------------------------
# Fonte de dados (local primeiro, senão google)
# ---------------------------
# Caminho local (fornecido a partir dos uploads — ajustar se necessário).
# OBS: este caminho existe no ambiente onde você subiu arquivos: usar conforme instruído.
LOCAL_DATA_PATH = "/mnt/data/PLANILHA REDESIM 2025 (Integrador).xlsx"

# URL de fallback (Google Sheets -> CSV export). Substitua pela planilha desejada se for o caso.
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1pk_X_h-tfpA53te1ViXcrY40SqSSI6WA/export?format=csv"

@st.cache_data(ttl=600)
def carregar_dados(local_path: str | None = None, gsheet_csv_url: str | None = None) -> pd.DataFrame:
    """Carrega dados: prioriza arquivo local (Excel/CSV), senão tenta o CSV do Google Sheets.
       Retorna DataFrame com todas as colunas como strings inicialmente para evitar inferências problemáticas.
    """
    df = pd.DataFrame()
    # 1) tenta arquivo local
    if local_path:
        try:
            if os.path.exists(local_path):
                # tenta excel primeiro
                try:
                    df = pd.read_excel(local_path, dtype=str)
                except Exception:
                    # fallback CSV read
                    df = pd.read_csv(local_path, dtype=str)
                return df
        except Exception:
            # segue para tentar google
            pass

    # 2) tenta google sheet csv (url já em formato export?format=csv)
    if gsheet_csv_url:
        try:
            df = pd.read_csv(gsheet_csv_url, dtype=str)
            return df
        except Exception:
            # retorna vazio se falhar
            return pd.DataFrame()

    return pd.DataFrame()

# carregar
df = carregar_dados(local_path=LOCAL_DATA_PATH, gsheet_csv_url=GSHEET_URL)

if df is None or df.empty:
    st.error("Dados não encontrados (arquivo local ausente e/ou planilha online inacessível).")
    st.stop()

# ---------------------------
# Normalização de nomes de coluna e utilitários
# ---------------------------
def normalize(col_name: str) -> str:
    if not isinstance(col_name, str):
        return ""
    s = col_name.strip().upper()
    # remove acentos básicos (suficiente para PT-BR)
    replacements = {
        "Á":"A","À":"A","Ã":"A","Â":"A",
        "É":"E","Ê":"E",
        "Í":"I",
        "Ó":"O","Õ":"O","Ô":"O",
        "Ú":"U",
        "Ç":"C"
    }
    for k,v in replacements.items():
        s = s.replace(k, v)
    s = s.replace(" ", "_").replace(".", "").replace("-", "_").replace("/", "_")
    return s

# preserva map original -> normalized
orig_cols = list(df.columns)
norm_map = {normalize(c): c for c in orig_cols}
# rename DataFrame columns to normalized names for trabalho interno
df = df.rename(columns={orig: normalize(orig) for orig in orig_cols})

# ---------------------------
# Detectores flexíveis de colunas
# ---------------------------
def detectar(df: pd.DataFrame, candidatos: list[str]) -> str | None:
    """Retorna o nome normalizado da primeira coluna que casar com candidatos (cada candidato pode ser nome com ou sem acento)."""
    candidatos_norm = [normalize(x) for x in candidatos]
    for cand in candidatos_norm:
        if cand in df.columns:
            return cand
    return None

# colunas importantes — tentativas de nomes variados
COL_LOCALIDADE = detectar(df, ["LOCALIDADE", "BAIRRO", "AREA", "TERRITORIO", "TERRITÓRIO"])
COL_CLASSIFICACAO = detectar(df, ["CLASSIFICACAO", "CLASSIFICAÇÃO", "STATUS", "TIPO", "CLASS"])
COL_SEXO = detectar(df, ["SEXO", "GENERO", "GÊNERO"])
COL_RACA = detectar(df, ["RACA_COR", "RAÇA_COR", "RACA", "COR", "RACA/COR"])
COL_GESTANTE = detectar(df, ["GESTANTE", "GRAVIDEZ", "GESTACAO"])
# coluna de data da notificação (tentativas comuns)
COL_DATA = detectar(df, [
    "DATA_NOTIFICACAO", "DATA_DE_NOTIFICACAO", "NOTIFICACAO", "DATA", "DATA_DO_CASO", "DATA_ENTRADA",
    "DATA_NOTIF", "DATE"
])

# ---------------------------
# Remover colunas sensíveis (qualquer coluna cujo nome contenha termos sensíveis)
# ---------------------------
sensiveis_tokens = ["NOME", "PACIENTE", "MAE", "MAE_", "RUA", "ENDERECO", "ENDEREÇO", "TELEFONE", "CELULAR", "CPF"]
# também esconder variações de data de nascimento
sensiveis_tokens += ["DATA_DE_NASCIMENTO", "NASCIMENTO", "DN", "DATA_NASC"]

cols_para_remover = [c for c in df.columns if any(tok in c for tok in sensiveis_tokens)]
# Não removemos colunas importantes (localidade, data, etc.) mesmo que contivessem tokens acidentais:
cols_para_remover = [c for c in cols_para_remover if c not in {COL_LOCALIDADE, COL_DATA}]

# efetiva remoção física dos dados sensíveis do df usado na tabela final (mantemos no df original para cálculos se precisar)
df = df.drop(columns=cols_para_remover, errors="ignore")

# ---------------------------
# Tratar coluna de data (criar MES e SEMANA EPIDEMIOLOGICA)
# ---------------------------
if COL_DATA and COL_DATA in df.columns:
    # converte para datetime
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], dayfirst=True, errors="coerce")
    # mês (YYYY-MM) para análise temporal
    df["MES_NOTIF"] = df[COL_DATA].dt.to_period("M").astype(str)
    # semana epidemiológica usando isocalendar week (string)
    # isocalendar is available in pandas >= 1.1 as dt.isocalendar().week
    try:
        df["SE_SEMANA"] = df[COL_DATA].dt.isocalendar().week.astype("Int64").astype(str)
    except Exception:
        # fallback: week via dt.week (deprecated), but try:
        df["SE_SEMANA"] = df[COL_DATA].dt.week.astype(str)
else:
    df["MES_NOTIF"] = "SEM_DATA"
    df["SE_SEMANA"] = "SEM_SEMANA"

# ---------------------------
# Sidebar: filtros (com opções seguras)
# ---------------------------
st.sidebar.header("Filtros")

# opcões seguras: checar existência de colunas antes de criar lista
def opcoes(col):
    if col and col in df.columns:
        # retornar valores únicos sem NaN
        return sorted(df[col].dropna().unique().tolist())
    return []

localidades = opcoes(COL_LOCALIDADE)
classificacoes = opcoes(COL_CLASSIFICACAO)
sexos = opcoes(COL_SEXO)
racas = opcoes(COL_RACA)
semanas = opcoes("SE_SEMANA")

# widgets
f_localidade = st.sidebar.multiselect("Localidade", options=localidades, default=localidades)
f_classificacao = st.sidebar.multiselect("Classificação", options=classificacoes, default=classificacoes)
f_sexo = st.sidebar.multiselect("Sexo", options=sexos, default=sexos)
f_raca = st.sidebar.multiselect("Raça/Cor", options=racas, default=racas)
f_semana = st.sidebar.multiselect("Semana Epidemiológica", options=semanas, default=semanas)

# construir df filtrado
df_filtrado = df.copy()
if f_localidade and COL_LOCALIDADE in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado[COL_LOCALIDADE].isin(f_localidade)]
if f_classificacao and COL_CLASSIFICACAO in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado[COL_CLASSIFICACAO].isin(f_classificacao)]
if f_sexo and COL_SEXO in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado[COL_SEXO].isin(f_sexo)]
if f_raca and COL_RACA in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado[COL_RACA].isin(f_raca)]
if f_semana and "SE_SEMANA" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["SE_SEMANA"].isin(f_semana)]

# ---------------------------
# Indicadores principais
# ---------------------------
st.header("📊 Indicadores Rápidos")
c1, c2 = st.columns(2)
c1.metric("Registros (filtrados)", len(df_filtrado))

if COL_GESTANTE and COL_GESTANTE in df_filtrado.columns:
    gestantes = df_filtrado[COL_GESTANTE].astype(str).str.contains("SIM", case=False, na=False).sum()
    c2.metric("Gestantes identificadas", gestantes)
else:
    c2.metric("Gestantes identificadas", "—")

# ---------------------------
# GRÁFICOS (usando MES_NOTIF — Data da Notificação)
# ---------------------------
st.markdown("## 📈 Séries Temporais")

# 1) Casos por mês (linha)
st.subheader("Casos por Mês")

if "MES_NOTIF" in df_filtrado.columns:
    series = (
        df_filtrado
        .groupby("MES_NOTIF")
        .size()
        .reset_index(name="CASOS")
        .sort_values("MES_NOTIF")
    )
    # garantir que MES_NOTIF esteja em formato ordenável (YYYY-MM)
    # construir figura de linha
    fig_mes = px.line(
        series,
        x="MES_NOTIF",
        y="CASOS",
        markers=True,
        title="Evolução mensal dos casos ",
        labels={"MES_NOTIF": "Mês (YYYY-MM)", "CASOS": "Casos"}
    )
    fig_mes.update_layout(xaxis=dict(tickangle=-45))
    st.plotly_chart(fig_mes, use_container_width=True)
else:
    st.warning("Coluna de mês (a partir da data de notificação) não encontrada.")

# 2) Classificação por mês (linhas separadas por classificação)
st.subheader("Classificação por Mês (Data da Notificação)")

if "MES_NOTIF" in df_filtrado.columns and COL_CLASSIFICACAO in df_filtrado.columns:
    class_mes = (
        df_filtrado
        .groupby(["MES_NOTIF", COL_CLASSIFICACAO])
        .size()
        .reset_index(name="CASOS")
    ).sort_values("MES_NOTIF")
    fig_class = px.line(
        class_mes,
        x="MES_NOTIF",
        y="CASOS",
        color=COL_CLASSIFICACAO,
        markers=True,
        title="Classificação por Mês",
        labels={"MES_NOTIF": "Mês (YYYY-MM)", "CASOS": "Casos"}
    )
    fig_class.update_layout(xaxis=dict(tickangle=-45))
    st.plotly_chart(fig_class, use_container_width=True)
else:
    st.warning("Não há dados suficientes para gerar 'Classificação por Mês' (verifique coluna de Data e Classificação).")

# 3) Distribuição por Localidade (barras agrupadas por classificação)
if COL_LOCALIDADE and COL_CLASSIFICACAO and COL_LOCALIDADE in df_filtrado.columns:
    st.subheader("Distribuição por Localidade")
    loc_summary = (
        df_filtrado
        .groupby([COL_LOCALIDADE, COL_CLASSIFICACAO])
        .size()
        .reset_index(name="CASOS")
        .sort_values("CASOS", ascending=False)
    )
    fig_loc = px.bar(
        loc_summary,
        x=COL_LOCALIDADE,
        y="CASOS",
        color=COL_CLASSIFICACAO,
        barmode="group",
        title="Localidade x Classificação"
    )
    st.plotly_chart(fig_loc, use_container_width=True)

# 4) Gráfico de Sexo (pizza) — sem relação temporal
if COL_SEXO and COL_SEXO in df_filtrado.columns:
    st.subheader("Distribuição por Sexo")
    sex_summary = df_filtrado[COL_SEXO].value_counts().reset_index()
    sex_summary.columns = [COL_SEXO, "QTD"]
    fig_sex = px.pie(sex_summary, names=COL_SEXO, values="QTD", title="Sexo")
    st.plotly_chart(fig_sex, use_container_width=True)

# 5) Raça/Cor x Sexo (cruzamento)
if COL_RACA and COL_SEXO and COL_RACA in df_filtrado.columns and COL_SEXO in df_filtrado.columns:
    st.subheader("Raça/Cor por Sexo")
    cruz = df_filtrado.groupby([COL_RACA, COL_SEXO]).size().reset_index(name="QTD")
    fig_raca_sexo = px.bar(
        cruz,
        x=COL_RACA,
        y="QTD",
        color=COL_SEXO,
        barmode="group",
        title="Raça/Cor por Sexo"
    )
    st.plotly_chart(fig_raca_sexo, use_container_width=True)

# ---------------------------
# TABELA FINAL: ocultar MES_NOTIF e colunas sensíveis (já removidas antes)
# ---------------------------
st.markdown("## 📋 Dados Filtrados")

# colunas a ocultar explicitamente
ocultar = ["MES_NOTIF", "SE_SEMANA"]
df_exib = df_filtrado.drop(columns=[c for c in ocultar if c in df_filtrado.columns], errors="ignore")

# garantir que não haja colunas de nascimento exibidas
df_exib = df_exib[[c for c in df_exib.columns if "NASC" not in c.upper() and "DATA_DE_NASC" not in c.upper()]]

st.dataframe(df_exib.reset_index(drop=True), use_container_width=True)

st.markdown("---")

st.caption("Painel de Oropouche • Versão 1.0")
st.caption("Desenvolvido por Maviael Barros.")
