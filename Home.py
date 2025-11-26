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
# SIDEBAR — LOGO + BUSCADOR + SOBRE
# ============================================================
with st.sidebar:

    # LOGO DO CIEVS NO TOPO
    st.image(
        "https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640",
        width=160
    )

    st.markdown("## 📍 Navegação")
    st.info("Use o menu acima para acessar os módulos do sistema.")

    st.markdown("---")

    # SEÇÃO SOBRE
    st.markdown("## 📘 Sobre este painel")
    st.markdown("""
O **Painel Integrado de Vigilância em Saúde do Ipojuca** é uma ferramenta estratégica
desenvolvida para fortalecer a gestão, qualificar análises e ampliar a capacidade de resposta
do município.

Aqui, dados se convertem em direção.  
Indicadores se transformam em ação.  
E cada visualização ilumina o caminho da saúde pública no território ipojucano.

Este ambiente integra informações da Vigilância Epidemiológica,  
Vigilância em Saúde do Trabalhador, Vigilância Sanitária e Vigilância Ambiental,
promovendo uma visão unificada, inteligente e estratégica do território.
    """)

    st.markdown("---")
    st.caption("Prefeitura do Ipojuca • Secretaria Municipal de Saúde")

# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================

col_logo, col_title = st.columns([1, 3])

with col_title:
    st.title("🏥 Painel Integrado de Vigilância em Saúde – Ipojuca")
    st.markdown(
        "Sistema oficial de monitoramento, análise e inteligência em saúde pública."
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
