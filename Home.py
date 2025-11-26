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
# CSS — Identidade visual da Prefeitura do Ipojuca
# ============================================================

st.markdown(
    """
    <style>

        /* ==============================
           CORES INSTITUCIONAIS
           ============================== */

        :root {
            --ipojuca-blue: #004F9F;
            --ipojuca-blue-light: #1A73E8;
            --light-bg: #F5F7FA;
            --dark-bg: #1a1a1a;
            --block-light: rgba(255,255,255,0.8);
            --block-dark: rgba(255,255,255,0.05);
        }

        /* ==============================
           GLOBAL — AJUSTES DE TEXTO
           ============================== */

        @media (prefers-color-scheme: light) {
            :root {
                --text-color: #1a1a1a;
                --text-color2: #333333;
                --block-bg: var(--block-light);
            }
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #ffffff;
                --text-color2: #dddddd;
                --block-bg: var(--block-dark);
            }
        }

        /* Fundo geral */
        .stApp {
            background: var(--light-bg);
        }
        @media (prefers-color-scheme: dark) {
            .stApp {
                background: var(--dark-bg);
            }
        }

        /* ==============================
           TÍTULO PRINCIPAL
           ============================== */

        .main-title-container {
            width: 100%;
            padding: 25px 10px 10px 5px;
        }

        .main-title {
            font-size: 42px;
            font-weight: 900;
            color: var(--ipojuca-blue-light);
            margin-bottom: 3px;
        }

        .main-subtitle {
            font-size: 22px;
            color: var(--text-color2);
            margin-top: -5px;
        }

        /* ==============================
           CARDS MODULARES
           ============================== */

        .module-card {
            padding: 22px;
            border-radius: 12px;
            background: var(--block-bg);
            border: 2px solid var(--ipojuca-blue);
            transition: 0.3s;
        }

        .module-card:hover {
            transform: scale(1.02);
            border-color: var(--ipojuca-blue-light);
        }

        /* ==============================
           LINKS INSTITUCIONAIS
           ============================== */

        .inst-card {
            padding: 18px;
            border-radius: 12px;
            background: var(--block-bg);
            border: 1px solid var(--ipojuca-blue);
            text-align: center;
        }

        /* ==============================
           SIDEBAR — FUNDO BRANCO PARA A LOGO
           ============================== */

        .sidebar-logo-container {
            background: white;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR — LOGO + SOBRE
# ============================================================
with st.sidebar:

    # Fundo branco para garantir legibilidade em modo escuro/claro
    st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
    st.image(
        "https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640",
        width=160
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## 📍 Navegação")
    st.info("Use o menu acima para acessar os módulos do sistema.")

    st.markdown("---")

    st.markdown("## 📘 Sobre este painel")
    st.markdown("""
O **Painel Integrado de Vigilância em Saúde do Ipojuca** é uma ferramenta estratégica  
para fortalecer análises, orientar decisões e ampliar a capacidade de resposta do município.  

Aqui, dados ganham sentido.  
Indicadores viram estratégia.  
E a inteligência em saúde guia o cuidado no território.  

Integra informações da Vigilância Epidemiológica,  
Saúde do Trabalhador, Vigilância Sanitária e Vigilância Ambiental,  
oferecendo uma visão unificada e profunda da saúde de Ipojuca.
    """)

    st.markdown("---")
    st.caption("Prefeitura do Ipojuca • Secretaria Municipal de Saúde")


# ============================================================
# TÍTULO PRINCIPAL — OCUPANDO TODA A LARGURA
# ============================================================

st.markdown(
    """
    <div class="main-title-container">
        <div class="main-title">
            🏥 Painel Integrado de Vigilância em Saúde – Ipojuca
        </div>
        <div class="main-subtitle">
            Sistema oficial de monitoramento, análise e inteligência em saúde pública.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# TEXTO DE BOAS-VINDAS
# ============================================================
st.markdown("""
Bem-vindo ao **Painel Integrado de Vigilância em Saúde**,  
onde a gestão encontra precisão, o cuidado encontra direção  
e o território descobre caminhos.  

Aqui, cada número pulsa.  
Cada gráfico respira.  
Cada indicador ilumina o futuro do SUS em Ipojuca.
""")

st.markdown("---")

# ============================================================
# MÓDULOS DISPONÍVEIS
# ============================================================
st.subheader("📊 Módulos Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='module-card'>
        <h3>🦟 Módulo de Dengue</h3>
        <ul>
            <li>Distribuição temporal</li>
            <li>Análise geográfica</li>
            <li>Indicadores epidemiológicos</li>
            <li>Perfil dos casos</li>
        </ul>
        <i>Acesse pelo menu lateral.</i>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='module-card'>
        <h3>👷 Saúde do Trabalhador</h3>
        <ul>
            <li>Indicadores principais</li>
            <li>Análises por ocupação</li>
            <li>Tendência temporal</li>
            <li>Distribuição territorial</li>
            <li>Evolução dos casos</li>
        </ul>
        <i>Acesse pelo menu lateral.</i>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='module-card'>
        <h3>🧪 Vigilância Sanitária (VISA)</h3>
        <ul>
            <li>Indicadores de 30 e 90 dias</li>
            <li>Produção mensal</li>
            <li>Análise por coordenação</li>
            <li>Processos abertos e concluídos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='module-card'>
        <h3>🦟 Oropouche</h3>
        <ul>
            <li>Distribuição por localidade</li>
            <li>Classificação dos casos</li>
            <li>Indicadores em gestantes</li>
            <li>Tendência por período</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# LINKS INSTITUCIONAIS
# ============================================================
st.subheader("🌐 Acesse também")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🔵 CIEVS Ipojuca</h3>
            <a href='https://cievsipojuca.wordpress.com/' target='_blank'>Acessar</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🟢 VISATT</h3>
            <a href='https://visattipojuca.com/' target='_blank'>Acessar</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class='inst-card'>
            <h3>🟣 Prefeitura do Ipojuca</h3>
            <a href='https://ipojuca.pe.gov.br/' target='_blank'>Acessar</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ============================================================
# COMO UTILIZAR + INFORMAÇÕES
# ============================================================
st.subheader("📌 Como utilizar este painel")

st.markdown("""
- Navegue pelos módulos usando o **menu lateral**.  
- Aplique filtros específicos em cada página.  
- Utilize gráficos e indicadores para análise territorial e temporal.  
- Exporte dados quando necessário.  
""")

st.markdown("---")

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
em parceria com as Gerências da Vigilância em Saúde.
""")
