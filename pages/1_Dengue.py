/* ===========================
   MODO ESCURO: DROPDOWN azul claro + texto branco
   =========================== */
@media (prefers-color-scheme: dark) {

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stMultiSelect * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[role="listbox"],
    [data-testid="stSidebar"] ul[role="listbox"] {
        background-color: #0073CF !important;
    }

    [data-testid="stSidebar"] div[role="listbox"] *,
    [data-testid="stSidebar"] ul[role="listbox"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[role="option"],
    [data-testid="stSidebar"] li[role="option"] {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[role="option"][aria-selected="true"],
    [data-testid="stSidebar"] li[role="option"][aria-selected="true"] {
        background-color: rgba(0,0,0,0.2) !important;
        color: #FFFFFF !important;
    }
}
