import streamlit as st

# IMPORTANTE: set_page_config deve ser a PRIMEIRA linha de código Streamlit
st.set_page_config(
    page_title="Painel de Saúde",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏥 Painel de Indicadores de Saúde")

st.markdown("""
## Bem-vindo ao Sistema de Monitoramento

Este painel apresenta indicadores e análises sobre:

### 📊 Módulos Disponíveis

1. **Dengue** - Análise de casos de dengue
   - Distribuição temporal de casos
   - Análise geográfica
   - Indicadores epidemiológicos

2. **Saúde do Trabalhador** - Monitoramento de acidentes de trabalho
   - Estatísticas de acidentes
   - Análise por setor
   - Tendências temporais

---

### 📌 Como usar

Utilize o menu lateral para navegar entre os diferentes módulos do sistema.

### ℹ️ Informações

- **Versão:** 1.0
- **Última atualização:** 2024
- **Desenvolvido com:** Streamlit + Python

---

*Selecione um módulo no menu lateral para começar.*
""")

# Sidebar
with st.sidebar:
    st.header("Navegação")
    st.info("Selecione uma página acima para visualizar os dados.")

    st.markdown("---")
    st.markdown("### Sobre")
    st.markdown("Sistema de monitoramento de indicadores de saúde pública.")
