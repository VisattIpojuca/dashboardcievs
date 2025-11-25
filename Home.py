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
# CABEÇALHO COM IMAGEM DO CIEVS
# ============================================================

col_logo, col_title = st.columns([1, 3])

with col_logo:
    st.image(
        "https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640",
        width=180
    )

with col_title:
    st.title("🏥 Painel Integrado de Vigilância em Saúde – Ipojuca")
    st.markdown(
        "Sistema integrado para monitoramento de indicadores epidemiológicos e de Saúde do Trabalhador."
    )

st.markdown("---")

# ============================================================
# TEXTO DE BOAS-VINDAS
# ============================================================

st.markdown("""
Seja bem-vindo ao **Painel Integrado de Indicadores da Vigilância em Saúde**,  
um ambiente onde cada dado vira direção, e cada indicador ilumina o caminho da gestão. ✨

Aqui você encontra informações estratégicas, atualizadas e organizadas  
para apoiar decisões, fortalecer ações e ampliar o impacto do SUS no território.
""")

st.markdown("---")

# ============================================================
# SEÇÃO: MÓDULOS DISPONÍVEIS
# ============================================================

st.subheader("📊 Módulos Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🦟 Módulo de Dengue  
    Monitoramento contínuo das arboviroses com dados de notificação:

    - 📅 Distribuição temporal  
    - 🗺️ Análise geográfica por bairro e distrito  
    - 📈 Indicadores epidemiológicos  
    - 👥 Perfil dos casos  

    *Acesse pelo menu lateral esquerdo.*
    """)

with col2:
    st.markdown("""
    ### 👷 Módulo de Saúde do Trabalhador  
    Acompanhamento dos acidentes de trabalho notificados no município:

    - 📌 Indicadores principais  
    - 🧑‍🏭 Análises por ocupação  
    - 🗓️ Tendência temporal  
    - 🏘️ Distribuição territorial  
    - 🩺 Evolução dos casos

    *Disponível no menu lateral esquerdo.*
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
- Navegue pelos módulos através do **menu lateral**.  
- Aplique filtros específicos em cada página para análises mais detalhadas.  
- Baixe dados filtrados quando disponível.  
- Utilize os gráficos para identificar tendências, padrões e anomalias.  
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
Desenvolvido com ❤️ utilizando **Streamlit**, **Python**,  
e dados das Gerências da Vigilância em Saúde de Ipojuca.
""")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("📍 Navegação")
    st.info("Use o menu acima para acessar os módulos do sistema.")

    st.markdown("---")
    st.subheader("🧭 Sobre este painel")
    st.markdown("Sistema integrado para monitoramento dos principais indicadores de saúde pública municipal.")
