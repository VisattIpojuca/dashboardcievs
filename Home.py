import streamlit as st

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA — precisa ser a primeira chamada!
# ========================================================================
st.set_page_config(
    page_title="Painel de Saúde Ipojuca",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# CSS – Ajuste de modo escuro/claro e visual institucional
# ========================================================================
st.markdown(
    """
    <style>
        /* Fundo transparente para blocos padrões */
        .css-1r6slb0, .css-12ttj6m, .stApp {
            background-color: transparent !important;
        }

        /* Título principal */
        .main-title {
            font-size: 45px;
            font-weight: 900;
            color: var(--text-color);
            margin-bottom: -5px;
        }

        .main-subtitle {
            font-size: 22px;
            margin-top: 5px;
            color: var(--text-color-secondary);
        }

        /* Cores adaptáveis ao modo claro/escuro */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #ffffff;
                --text-color-secondary: #cccccc;
            }
        }
        @media (prefers-color-scheme: light) {
            :root {
                --text-color: #1a1a1a;
                --text-color-secondary: #333333;
            }
        }

        /* Cartões de módulos */
        .module-card {
            padding: 25px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(0,0,0,0.1);
            transition: 0.3s;
        }
        @media (prefers-color-scheme: dark) {
            .module-card {
                background: rgba(40, 40, 40, 0.6);
                border: 1px solid rgba(255,255,255,0.1);
            }
        }

        .module-card:hover {
            transform: scale(1.01);
            border-color: #2a71d0;
        }

        /* Links institucionais */
        .inst-card {
            padding: 20px;
            border-radius: 12px;
            background: rgba(255,255,255,0.75);
            text-align: center;
            border: 1px solid rgba(0,0,0,0.1);
        }
        @media (prefers-color-scheme: dark) {
            .inst-card {
                background: rgba(50,50,50,0.65);
            }
        }
        .inst-card a {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ========================================================================
# TÍTULO PRINCIPAL – ocupa toda a largura
# ========================================================================

st.markdown(
    """
    <div style='padding: 10px 0 25px 0;'>
        <div class="main-title">🏥 Painel Integrado de Vigilância em Saúde – Ipojuca</div>
        <div class="main-subtitle">
            Sistema oficial de monitoramento, análise e inteligência em saúde pública.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ========================================================================
# TEXTO DE BOAS-VINDAS
# ========================================================================
st.markdown(
    """
    Seja bem-vindo ao **Painel Integrado de Indicadores da Vigilância em Saúde**,  
    um ambiente onde cada número se transforma em estratégia,  
    e cada gráfico ajuda a desenhar o futuro do cuidado. ✨  

    Aqui você encontra informações estratégicas, atualizadas e organizadas  
    para apoiar decisões, fortalecer ações e ampliar o impacto do SUS no território.
    """
)

st.markdown("---")

# ========================================================================
# SEÇÃO — MÓDULOS DISPONÍVEIS
# ========================================================================
st.subheader("📊 Módulos Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class='module-card'>
            <h3>🦟 Módulo de Dengue</h3>
            <ul>
                <li>📅 Distribuição temporal dos casos</li>
                <li>🗺️ Análise geográfica por bairro</li>
                <li>📈 Indicadores epidemiológicos</li>
                <li>👥 Perfil dos casos</li>
            </ul>
            <i>Acesse pelo menu lateral esquerdo.</i>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class='module-card'>
            <h3>👷 Módulo de Saúde do Trabalhador</h3>
            <ul>
                <li>📌 Indicadores principais</li>
                <li>🧑‍🏭 Análise por ocupação</li>
                <li>🗓️ Tendência temporal</li>
                <li>🏘️ Distribuição territorial</li>
                <li>🩺 Evolução dos casos</li>
            </ul>
            <i>Acesse pelo menu lateral esquerdo.</i>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ========================================================================
# LINKS INSTITUCIONAIS
# ========================================================================
st.subheader("🌐 Acesse também")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🔵 CIEVS Ipojuca</h3>
            <a href="https://cievsipojuca.wordpress.com/" target="_blank">
                👉 Acessar site
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🟢 VISATT Ipojuca</h3>
            <a href="https://visattipojuca.com/" target="_blank">
                👉 Acessar site
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🟣 Prefeitura do Ipojuca</h3>
            <a href="https://ipojuca.pe.gov.br/" target="_blank">
                👉 Acessar site
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ========================================================================
# COMO UTILIZAR + SOBRE O PAINEL (texto unificado)
# ========================================================================
st.subheader("📌 Como utilizar este painel")

st.markdown(
    """
    - Navegue pelos módulos através do **menu lateral esquerdo**.  
    - Utilize os filtros para análises personalizadas e mais profundas.  
    - Baixe os dados filtrados quando a opção estiver disponível.  
    - Explore gráficos, tendências e indicadores para subsidiar decisões.  
    """
)

st.subheader("ℹ️ Sobre este painel")

st.markdown(
    """
    O Painel Integrado de Vigilância em Saúde de Ipojuca é uma ferramenta estratégica  
    desenvolvida para apoiar a gestão municipal, integrando dados da Vigilância Epidemiológica,  
    Vigilância Ambiental, Vigilância Sanitária, Saúde do Trabalhador e CIEVS.  

    Ele foi desenhado para oferecer **clareza, velocidade e profundidade analítica**,  
    respeitando a proteção de dados e valorizando a inteligência em saúde.  
    """
)

st.markdown("---")

# ========================================================================
# INFORMAÇÕES DO SISTEMA
# ========================================================================
st.subheader("📘 Informações do Sistema")

cA, cB, cC = st.columns(3)

with cA:
    st.metric("Versão", "1.0")

with cB:
    st.metric("Atualização", "2025")

with cC:
    st.metric("Responsável", "Vigilância em Saúde – Ipojuca")

st.markdown(
    """
    Desenvolvido com ❤️ utilizando **Python**, **Streamlit**,  
    e dados fornecidos pelas Gerências da Vigilância em Saúde – Ipojuca.
    """
)

# ========================================================================
# SIDEBAR
# ========================================================================
with st.sidebar:
    st.header("📍 Navegação")
    st.info("Use o menu acima para acessar os módulos do sistema.")

    st.markdown("---")
    st.subheader("🧭 Sobre")
    st.markdown("Sistema integrado de monitoramento da saúde pública municipal.")
