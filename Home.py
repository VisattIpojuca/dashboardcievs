import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA — precisa ser a primeira chamada!
# ============================================================
st.set_page_config(
    page_title="Painel de Saúde Ipojuca",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — IDENTIDADE VISUAL FIXA (SEM MUDAR NO DARK MODE)
# ============================================================

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

/* ====== FORÇAR COR DO TEXTO (fixo em preto no modo claro/escuro) ====== */
html, body, [data-testid="stAppViewContainer"], * {
    color: #000000 !important;
}

/* Títulos (cor fixa) */
h1, h2, h3, h4, h5, h6 {
    color: var(--verde-ipojuca) !important;
}

/* Parágrafos */
p {
    color: #000 !important;
    text-align: justify !important;
}

/* Listas */
li {
    color: #000 !important;
}

/* Textos informativos */
span, label, div, section {
    color: #000 !important;
}

/* Inputs e seus textos */
input, textarea, select {
    color: #000 !important;
}

/* Botões */
button, .stButton button {
    color: #000 !important;
}

/* Links */
a {
    color: var(--azul-secundario) !important;
    font-weight: 600;
}

/* ====== FUNDO GERAL FIXO ====== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
}

/* ====== SIDEBAR FIXA ====== */
[data-testid="stSidebar"] {
    background: var(--azul-principal) !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Links na sidebar */
[data-testid="stSidebar"] a {
    color: #004A8D !important;
}

/* ====== CARDS ====== */
.stMetric {
    background-color: var(--amarelo-ipojuca) !important;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid var(--azul-secundario);
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}

/* ====== QUADRO DA LOGO ====== */
.sidebar-logo {
    background:white;
    padding:10px;
    border-radius:10px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR — LOGO DENTRO DE QUADRO BRANCO
# ============================================================

with st.sidebar:

    st.markdown("""
        <div class="sidebar-logo">
            <img src="https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640"
                 width="150">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📍 Navegação")
    st.info("Use o menu acima para acessar os módulos do sistema.")

    st.markdown("---")

    # SEÇÃO SOBRE
    st.markdown("## 📘 Sobre este painel")
    st.markdown("""
O **Painel Integrado de Vigilância em Saúde do Ipojuca** é uma plataforma estratégica
para análise, inteligência e monitoramento situacional do território.

Ele unifica os principais sistemas de vigilância — Epidemiológica,  
Saúde do Trabalhador, Vigilância Sanitária e Vigilância Ambiental —  
em um ambiente visual, acessível e orientado à tomada de decisão.

Seu objetivo é fortalecer as ações municipais,  
qualificar a gestão da informação e iluminar caminhos  
para intervenções mais rápidas, eficientes e humanizadas.
    """)

    st.markdown("---")
    st.caption("Prefeitura do Ipojuca • Secretaria Municipal de Saúde")

# ============================================================
# CABEÇALHO PRINCIPAL — OCUPA TODA A LARGURA
# ============================================================

st.markdown("""
<div style="
    background: var(--azul-principal);
    padding: 35px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
">
    <h1 style="color:white; margin-bottom:0;">
        🏥 Painel Integrado de Vigilância em Saúde – Ipojuca
    </h1>
    <p style="font-size:1.2rem; margin-top:8px;">
        Sistema oficial de monitoramento, análise e inteligência em saúde pública.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TEXTO DE BOAS-VINDAS
# ============================================================

st.markdown("""
Bem-vindo ao **Painel Integrado de Indicadores da Vigilância em Saúde**,  
onde a gestão encontra precisão, o cuidado encontra direção  
e o território encontra respostas.

Aqui, cada número pulsa.  
Cada gráfico respira.  
Cada indicador revela caminhos  
para fortalecer o SUS em Ipojuca.
""")

st.markdown("---")

# ============================================================
# MÓDULOS DISPONÍVEIS
# ============================================================

st.subheader("📊 Módulos Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🦟 Módulo de Dengue  
    - Distribuição temporal  
    - Análise geográfica  
    - Indicadores epidemiológicos  
    - Perfil dos casos  
    """)

with col2:
    st.markdown("""
    ### 👷 Saúde do Trabalhador  
    - Indicadores principais  
    - Análises por ocupação  
    - Tendência temporal  
    - Territórios afetados  
    - Evolução dos casos  
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    ### 🧪 Vigilância Sanitária (VISA)
    - Indicadores de 30 e 90 dias  
    - Produção mensal  
    - Territorialização  
    - Processos pendentes e concluídos  
    """)

with col4:
    st.markdown("""
    ### 🦟 Oropouche  
    - Distribuição por localidade  
    - Classificação dos casos  
    - Indicadores em gestantes  
    - Tendência por período  
    """)

st.markdown("---")

# ============================================================
# LINKS INSTITUCIONAIS
# ============================================================

st.subheader("🌐 Acesse também")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### 🔵 CIEVS Ipojuca")
    st.markdown("[👉 Acessar site](https://cievsipojuca.wordpress.com/)")

with colB:
    st.markdown("### 🟢 VISATT Ipojuca")
    st.markdown("[👉 Acessar site](https://visattipojuca.com/)")

with colC:
    st.markdown("### 🟣 Prefeitura do Ipojuca")
    st.markdown("[👉 Acessar site](https://ipojuca.pe.gov.br/)")

st.markdown("---")

# ============================================================
# COMO UTILIZAR
# ============================================================

st.subheader("📌 Como utilizar este painel")

st.markdown("""
- Navegue pelos módulos usando o **menu lateral**.  
- Aplique filtros específicos em cada página.  
- Leia indicadores, tendências e distribuições.  
- Utilize exportações quando disponíveis.  
""")

st.markdown("---")

# ============================================================
# INFORMAÇÕES DO SISTEMA
# ============================================================

st.subheader("ℹ️ Informações do Sistema")

colA, colB, colC = st.columns(3)

with colA:
    st.metric("Versão", "1.0")

with colB:
    st.metric("Atualização", "2025")

with colC:
    st.metric("Responsável", "Vigilância em Saúde – Ipojuca")

st.markdown("""
Desenvolvido com ❤️ utilizando **Streamlit** e **Python**,  
em parceria com as gerências da Vigilância em Saúde do município.
""")
