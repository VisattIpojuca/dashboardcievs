import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Painel de Saúde Ipojuca",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — IDENTIDADE VISUAL INSTITUCIONAL
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

/* Fundo geral */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #F6F9FC, #EAF3FF) !important;
}

/* Texto principal área central */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown {
    color: #004A8D !important;
}

/* Títulos amarelos */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 800 !important;
}

/* Parágrafos justificados */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] li {
    text-align: justify !important;
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"] {
    background: var(--azul-principal) !important;
}

/* Navegação multipage em branco */
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
[data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] button[aria-current="page"],
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

/* Títulos na sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: var(--amarelo-ipojuca) !important;
    font-weight: 800 !important;
}

/* Texto sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

/* Links na sidebar */
[data-testid="stSidebar"] a {
    color: #FFFFFF !important;
    font-weight: 600;
}

/* Card da logo */
.sidebar-logo {
    background: #FFFFFF;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}

/* Métricas (cards informativos) */
.stMetric {
    background-color: var(--amarelo-ipojuca) !important;
    padding: 18px;
    border-radius: 10px;
    border-left: 6px solid var(--azul-secundario);
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}

/* Cards de módulos */
.modulo-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    border-left: 5px solid var(--azul-secundario);
    min-height: 170px;
}
.modulo-card h3 {
    margin-top: 0;
    margin-bottom: 6px;
    color: var(--azul-principal) !important;
}
.modulo-card p, .modulo-card li {
    color: #004A8D !important;
}

/* Cards de links institucionais (sem ícones coloridos) */
.link-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0px 1px 5px rgba(0,0,0,0.08);
    border-left: 4px solid var(--verde-ipojuca);
}
.link-card h3 {
    margin-top: 0;
    margin-bottom: 6px;
    color: var(--azul-principal) !important;
}
.link-card p, .link-card a {
    color: #004A8D !important;
}

/* Botões */
button, .stButton button {
    color: #FFFFFF !important;
    background-color: var(--azul-secundario) !important;
    border-radius: 6px !important;
}

/* Selo oficial no hero */
.hero-badge {
    display:inline-block;
    background: rgba(0,0,0,0.25);
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
}

/* Rodapé */
.footer-text {
    font-size: 0.85rem;
    color: #004A8D !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — LOGO + TEXTO CURTO
# ============================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <img src="https://cievsipojuca.wordpress.com/wp-content/uploads/2022/01/cievs-ipojuca-sem-fundo.png?w=640"
                 width="150">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📍 Navegação")
    st.info("Selecione, no menu acima, o módulo que deseja visualizar.")

    st.markdown("---")
    st.markdown("### 📘 Sobre o painel")
    st.markdown("""
    O **Painel Integrado de Vigilância em Saúde do Ipojuca** consolida,
    em um único ambiente, os principais indicadores estratégicos para
    apoio à gestão e à tomada de decisão em saúde pública.
    """)

    st.markdown("---")
    st.caption("Vigilância em Saúde • Cievs Ipojuca • MB Technological Solutions®")

# ============================================================
# HERO / CABEÇALHO PRINCIPAL
# ============================================================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #004A8D, #0073CF);
    padding: 32px;
    border-radius: 12px;
    color: white;
    margin-bottom: 28px;
">
       <h1 style="color:white; margin-top:10px; margin-bottom:4px;">
        🏥 Painel de Indicadores de Vigilância em Saúde – Ipojuca
  </div>
""", unsafe_allow_html=True)

# ============================================================
# TEXTO DE APRESENTAÇÃO
# ============================================================
st.markdown("""
O painel integra informações de diversos eixos da Vigilância em Saúde municipal —  Cievs Ipojuca,
vigilância epidemiológica, ambiental, sanitária e saúde do trabalhador e da trabalhadora,  —  
oferecendo uma visão consolidada da situação de saúde no território.

A partir dos módulos temáticos, é possível acompanhar tendências,
identificar áreas prioritárias, apoiar o planejamento de ações
e qualificar a resposta oportuna às demandas do SUS em Ipojuca.
""")

st.markdown("---")

# ============================================================
# MÓDULOS DISPONÍVEIS – EM FORMA DE CARDS
# ============================================================
st.subheader("📊 Módulos temáticos")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="modulo-card">
        <h3>🦟 Módulo de Dengue</h3>
        <ul>
            <li>Séries históricas e sazonalidade</li>
            <li>Distribuição espacial por bairro/localidade</li>
            <li>Indicadores epidemiológicos e perfil dos casos</li>
            <li>Subsídios para planejamento de ações de controle vetorial</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="modulo-card">
        <h3>👷 Saúde do Trabalhador</h3>
        <ul>
            <li>Notificações relacionadas ao trabalho</li>
            <li>Análises por ocupação, setor e atividade</li>
            <li>Tendência temporal de agravos</li>
            <li>Identificação de grupos e territórios mais vulneráveis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="modulo-card">
        <h3>🧪 Vigilância Sanitária (VISA)</h3>
        <ul>
            <li>Produção mensal de ações fiscalizatórias</li>
            <li>Indicadores de 30 e 90 dias</li>
            <li>Distribuição territorial dos estabelecimentos</li>
            <li>Acompanhamento de processos pendentes e concluídos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="modulo-card">
        <h3>🦟 Módulo de Oropouche</h3>
        <ul>
            <li>Monitoramento por localidade</li>
            <li>Classificação e evolução dos casos</li>
            <li>Indicadores específicos em gestantes</li>
            <li>Análise temporal por período e semana epidemiológica</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Linha seguinte com o PCE
c5, _ = st.columns([1, 1])

with c5:
    st.markdown("""
    <div class="modulo-card">
        <h3>🧬 Programa de Controle da Esquistossomose (PCE)</h3>
        <ul>
            <li>Monitoramento de exames e casos</li>
            <li>Distribuição espacial por área e localidade</li>
            <li>Acompanhamento de ciclos de busca ativa</li>
            <li>Indicadores para planejamento das ações de controle</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CANAIS INSTITUCIONAIS
# ============================================================
st.subheader("🌐 Canais institucionais")

l1, l2, l3 = st.columns(3)

with l1:
    st.markdown("""
    <div class="link-card">
        <h3>CIEVS Ipojuca</h3>
        <p>Informes, notas técnicas e documentos de referência em vigilância.</p>
        <p><a href="https://cievsipojuca.wordpress.com/" target="_blank">Acesse</a></p>
    </div>
    """, unsafe_allow_html=True)

with l2:
    st.markdown("""
    <div class="link-card">
        <h3>VISATT Ipojuca</h3>
        <p>Informações sobre saúde do trabalhador, notificações e orientações.</p>
        <p><a href="https://visattipojuca.com/" target="_blank">Acesse</a></p>
    </div>
    """, unsafe_allow_html=True)

with l3:
    st.markdown("""
    <div class="link-card">
        <h3>Prefeitura do Ipojuca</h3>
        <p>Portal oficial da gestão municipal, notícias e serviços.</p>
        <p><a href="https://ipojuca.pe.gov.br/" target="_blank">Acesse</a></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# COMO UTILIZAR / GOVERNANÇA
# ============================================================
st.subheader("📌 Orientações de uso")

st.markdown("""
- Utilize o **menu lateral** para acessar os módulos temáticos.  
- Em cada módulo, aplique os **filtros** disponíveis para refinar a análise.  
- Interprete os gráficos e indicadores à luz da realidade local.  
- Sempre que possível, complemente a leitura com dados qualitativos do território.  
""")

st.markdown("---")

st.subheader("ℹ️ Governança do painel")

cA, cB, cC, cD = st.columns(4)

with cA:
    st.metric("Versão do painel", "1.0")

with cB:
    st.metric("Ano de referência", "2025")

with cC:
    st.metric("Gestão responsável", "Cievs Ipojuca")

with cD:
    st.metric("Tecnologia", "MB Technological Solutions®")

st.markdown("""
<div class="footer-text">
Esta aplicação foi desenvolvida em parceria com o Centro de Informações Estratégicas 
em Vigilância em Saude de Ipojuca (Cievs Ipojuca) e as áreas técnicas da Vigilância 
em Saúde do município e <strong>MB Technological Solutions® (Maviael Barros Soluções 
Tecnológicas)</strong>, com o objetivo de fortalecer a gestão da informação e a 
transparência em saúde pública.
</div>
""", unsafe_allow_html=True)
