# ----------------------------------------------------------
# GRÁFICOS — fundo sempre branco e textos visíveis
# ----------------------------------------------------------

cores = ["#004A8D", "#009D4A", "#FFC20E", "#0073CF"]

st.header("📈 Distribuições")

# Sexo
if COL_SEXO:
    ds = df_filtrado[COL_SEXO].value_counts().reset_index()
    ds.columns = ["SEXO", "QTD"]
    fig = px.pie(
        ds,
        names="SEXO",
        values="QTD",
        title="Distribuição por Sexo",
        hole=0.3,
        color_discrete_sequence=cores
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Raça/cor x sexo
if COL_RACA and COL_SEXO:
    d = df_filtrado[[COL_RACA, COL_SEXO]].dropna()
    d = d.groupby([COL_RACA, COL_SEXO]).size().reset_index(name="QTD")
    fig = px.bar(
        d,
        x=COL_RACA,
        y="QTD",
        color=COL_SEXO,
        title="Raça/Cor por Sexo",
        color_discrete_sequence=cores,
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Idade
if COL_IDADE:
    fig = px.histogram(
        df_filtrado,
        x=COL_IDADE,
        title="Distribuição por Idade",
        color_discrete_sequence=[cores[0]]
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Escolaridade
if COL_ESCOLARIDADE:
    df_esc = df_filtrado[COL_ESCOLARIDADE].value_counts().reset_index()
    df_esc.columns = ["ESCOLARIDADE", "QTD"]
    fig = px.bar(
        df_esc,
        x="ESCOLARIDADE",
        y="QTD",
        title="Escolaridade",
        color_discrete_sequence=[cores[3]]
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Bairro
if COL_BAIRRO:
    df_bairro = df_filtrado[COL_BAIRRO].value_counts().reset_index()
    df_bairro.columns = ["BAIRRO", "QTD"]
    fig = px.bar(
        df_bairro.head(20),
        x="BAIRRO",
        y="QTD",
        title="Top 20 Bairros",
        color_discrete_sequence=[cores[1]]
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# Evolução
if COL_EVOL:
    df_ev = df_filtrado[COL_EVOL].value_counts().reset_index()
    df_ev.columns = ["EVOLUCAO", "QTD"]
    fig = px.bar(
        df_ev,
        x="EVOLUCAO",
        y="QTD",
        title="Evolução dos Casos",
        color_discrete_sequence=[cores[2]]
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
