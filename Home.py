import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA — deve ser a primeira instrução!
# ============================================================
st.set_page_config(
    page_title="Painel de Saúde de Ipojuca",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — Estilos inspirados na identidade visual oficial
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Montserrat:wght@600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3, .metric-label {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
}

.section-box {
    background-color: #f7f9fc;
    padding: 25px;
    border-radius: 12px;
    border-left: 6px solid #003F8C;  /* Azul Ipojuca */
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.big-separator {
    height: 6px;
    background: linear-gradient(90deg, #003F8C, #FFC72C, #009364);
    border-radius: 5px;
    margin-top: 15px;
    margin-bottom: 25px;
}

a {
    text-decoration: none;
    font-weight: 600;
    color: #003F8C;
}

a:hover {
    color: #009364;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CABEÇALHO COM LOGO
# ============================================================

col_logo, col_title = st.columns([1, 3])

with col_logo:
    st.image(
        "https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640",
        width=180
    )

with col_title:
    st.markdown("<h1>🏥 Painel Integrado de Vigilância em Saúde – Ipojuca</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size:18px;'>
        Monitoramento inteligente dos indicadores epidemiológicos e da Saúde do Trabalhador.  
        Um painel moderno, integrado e alinhado à identidade visual da gestão municipal.
        </p>
    """, unsafe_allow_html=True)

st.markdown("<div class='big-separator'></div>", unsafe_allow_html=True)

# ============================================================
# TEXTO DE APRESENTAÇÃO
# ============================================================

st.markdown("""
<div class='section-box'>
<h2>👋 Bem-vindo ao Painel Integrado de Vigilância em Saúde</h2>

Este painel é uma bússola digital da gestão:  
cada gráfico revela um movimento,  
cada filtro mostra um território,  
cada indicador acende um alerta.

Aqui, dados viram decisão.  
Aqui, gestão vira cuidado.

</div>
""", unsafe_allow_html=True)

# ============================================================
# MÓDULOS DISPONÍVEIS
# ============================================================

st.markdown("<h2>📊 Módulos do Sistema</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='section-box'>
    <h3>🦟 Módulo de Dengue</h3>
    <ul>
        <li>Distribuição temporal</li>
        <li>Análise territorial</li>
        <li>Perfil dos casos</li>
        <li>Indicadores epidemiológicos</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='section-box'>
    <h3>👷 Saúde do Trabalhador</h3>
    <ul>
        <li>Acompanhamento dos acidentes de trabalho</li>
        <li>Análises por ocupação</li>
        <li>Evolução dos casos</li>
        <li>Distribuição territorial</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# LINKS INSTITUCIONAIS
# ============================================================

st.markdown("<h2>🌐 Acesse também</h2>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("""
    <div class='section-box'>
    <h3>🔵 CIEVS Ipojuca</h3>
    <a href='https://cievsipojuca.wordpress.com/' target='_blank'>Acessar site</a>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class='section-box'>
    <h3>🟢 VISATT Ipojuca</h3>
    <a href='https://visattipojuca.com/' target='_blank'>Acessar site</a>
    </div>
    """, unsafe_allow_html=True)

with colC:
    st.markdown("""
    <div class='section-box'>
    <h3>🟣 Prefeitura do Ipojuca</h3>
    <a href='https://ipojuca.pe.gov.br/' target='_blank'>Acessar site</a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# COMO UTILIZAR
# ============================================================

st.markdown("<h2>📌 Como usar este painel</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='section-box'>
<ul>
    <li>Use o menu lateral para navegar entre os módulos.</li>
    <li>Aplique filtros para personalizar análises.</li>
    <li>Explore gráficos interativos para identificar padrões.</li>
    <li>Baixe dados filtrados quando disponível.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INFORMAÇÕES DO SISTEMA
# ============================================================

st.markdown("<h2>ℹ️ Informações do Sistema</h2>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)

with colA:
    st.metric("Versão", "1.0")

with colB:
    st.metric("Atualização", "2025")

with colC:
    st.metric("Responsável", "Vigilância em Saúde – Ipojuca")

st.markdown("""
<div class='section-box'>
Desenvolvido com ❤️ utilizando <b>Python</b>, <b>Streamlit</b>  
e dados das Gerências da Vigilância em Saúde do Município do Ipojuca.
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("📍 Navegação")
    st.info("Escolha um módulo no menu acima.")

    st.markdown("---")
    st.subheader("🧭 Sobre o painel")
    st.markdown("Sistema integrado para monitoramento dos principais indicadores de saúde pública municipal.")
