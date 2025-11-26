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

# ============================================================
# TEXTO DE BOAS-VINDAS
# ============================================================
st.markdown("""
Bem-vindo ao **Painel Integrado de Indicadores da Vigilância em Saúde**,  
onde a gestão encontra precisão, o cuidado encontra direção  
e o território encontra respostas.

Aqui, cada número pulsa.  
Cada gráfico respira.  
Cada indicador revela caminhos para fortalecer o SUS em Ipojuca.  
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
    Monitoramento contínuo das arboviroses:

    - Distribuição temporal  
    - Análise geográfica  
    - Indicadores epidemiológicos  
    - Perfil dos casos  

    *Acesse pelo menu lateral.*
    """)

with col2:
    st.markdown("""
    ### 👷 Saúde do Trabalhador  
    Acompanhamento dos acidentes de trabalho:

    - Indicadores principais  
    - Análises por ocupação  
    - Tendência temporal  
    - Territórios e setores afetados  
    - Evolução dos casos  

    *Acesse pelo menu lateral.*
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    ### 🧪 Vigilância Sanitária (VISA)
    Monitoramento da produção, inspeções, resultados e desempenho do serviço.

    - Indicadores de 30 e 90 dias  
    - Produção mensal  
    - Análise por coordenação e território  
    - Processos pendentes e concluídos  
    """)

with col4:
    st.markdown("""
    ### 🦟 Oropouche  
    Acompanhamento dos casos notificados:

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
# COMO UTILIZAR + SOBRE (VERSÃO RESUMIDA)
# ============================================================
st.subheader("📌 Como utilizar este painel")

st.markdown("""
- Navegue pelos módulos usando o **menu lateral**.  
- Aplique filtros específicos em cada página.  
- Leia indicadores, tendências e distribuições territoriais.  
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
em parceria com as Gerências da Vigilância em Saúde do município.
""")
