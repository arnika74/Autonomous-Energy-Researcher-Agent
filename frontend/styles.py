import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
            --primary-color: #00d4ff;
            --accent-color: #0099ff;
            --dark-bg: #0a0e27;
            --card-bg: rgba(15, 23, 42, 0.95);
            --text-primary: #e2e8f0;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: rgba(0, 212, 255, 0.1);
        }

        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 10px rgba(0, 212, 255, 0.3); }
            50% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            color: var(--text-primary);
            animation: fadeInDown 0.6s ease-out;
        }

        h1 {
            font-size: 4.5rem;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -1px;
        }

        h2 {
            font-size: 2.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #00d4ff;
        }

        h3 {
            font-size: 1.6rem;
            color: #0099ff;
            margin-top: 1.5rem;
        }

        .stMarkdown, p, span, li { color: var(--text-secondary); line-height: 1.7; font-size: 1.15rem; }
        .stCaption { color: var(--text-muted) !important; font-size: 0.95rem; }
        .stContainer, .element-container { animation: fadeInUp 0.5s ease-out; }

       /* Full expander box */
details {
    background: rgba(15, 23, 42, 0.95) !important;
    border: 1px solid rgba(0, 212, 255, 0.15) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    margin-bottom: 14px !important;
}

/* Expander header (Introduction / Key Findings / Conclusion) */
summary {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.06), rgba(0, 153, 255, 0.03)) !important;
    color: #00d4ff !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Header text color fix */
summary span {
    color: #00d4ff !important;
}

        .stTextInput input, .stTextArea textarea {
            background: rgba(30, 41, 59, 0.8) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease;
        }

        .stTextInput input::placeholder, .stTextArea textarea::placeholder { color: var(--text-muted) !important; }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #00d4ff !important;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
            background: rgba(30, 41, 59, 0.95) !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #00d4ff, #0099ff) !important;
            color: #0a0e27 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 32px !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        }

        /* removed hover transitions for static experience */
        .stButton > button:active { transform: translateY(0) !important; }

        .stAlert { border-radius: 12px !important; border-left: 4px solid !important; animation: slideInLeft 0.4s ease-out; }
        .stSuccess { background: rgba(34, 197, 94, 0.1) !important; border-color: #22c55e !important; }
        .stError { background: rgba(239, 68, 68, 0.1) !important; border-color: #ef4444 !important; }
        .stWarning { background: rgba(245, 158, 11, 0.1) !important; border-color: #f59e0b !important; }
        .stInfo { background: rgba(59, 130, 246, 0.1) !important; border-color: #3b82f6 !important; }

        .stSidebar { background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(20, 30, 50, 0.95) 100%) !important; border-right: 1px solid var(--border-color) !important; }
        .stSidebar .stMarkdown, .stSidebar p { color: var(--text-secondary); }
        .stSidebar h1, .stSidebar h2, .stSidebar h3 { color: #00d4ff; }
        .stSidebar .stButton > button { width: 100%; justify-content: left; text-align: left; margin-bottom: 8px; font-size: 0.95rem; background: rgba(0, 212, 255, 0.1) !important; color: #00d4ff !important; border: 1px solid rgba(0, 212, 255, 0.3) !important; }
        .stSidebar .stButton > button:hover { background: rgba(0, 212, 255, 0.2) !important; border-color: #00d4ff !important; }

        .stDivider { border-color: var(--border-color) !important; }
        pre, code { background: rgba(30, 41, 59, 0.8) !important; color: #00d4ff !important; border-radius: 8px !important; }
        .dataframe { background: var(--card-bg) !important; color: var(--text-secondary); border-radius: 8px !important; }
        a { color: #00d4ff !important; text-decoration: none; transition: all 0.2s ease; }
        a:hover { color: #0099ff !important; text-decoration: underline; }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 212, 255, 0.3); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 212, 255, 0.6); }

        .highlight-section { background: rgba(0, 212, 255, 0.05); border-left: 4px solid #00d4ff; padding: 16px; border-radius: 8px; margin: 16px 0; }

        header, [data-testid="stToolbar"] { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%) !important; border-bottom: 1px solid rgba(0, 212, 255, 0.1) !important; }
        button[kind="secondary"] { background: rgba(0, 212, 255, 0.1) !important; color: #00d4ff !important; border: 1px solid rgba(0, 212, 255, 0.3) !important; font-weight: 500 !important; }
        button[kind="secondary"]:hover { background: rgba(0, 212, 255, 0.2) !important; border-color: #00d4ff !important; }
        [data-testid="stToolbar"] span, [data-testid="stToolbar"] p { color: #cbd5e1 !important; }

        .streamlit-expanderHeader, .stMenu { background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(0, 153, 255, 0.03)) !important; color: #00d4ff !important; border: 1px solid rgba(0, 212, 255, 0.2) !important; }
        [role="menu"], [role="dialog"], .stPopup { background: linear-gradient(135deg, #0f1729 0%, #1a1f3a 100%) !important; border: 1px solid rgba(0, 212, 255, 0.3) !important; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important; outline: none !important; }
        [data-testid="stMenu"] { border: 1px solid rgba(0, 212, 255, 0.3) !important; outline: none !important; }
        .stPopover { border: 1px solid rgba(0, 212, 255, 0.3) !important; }
        .streamlit-container-scroller { border: none !important; }
        [role="menu"] button, [role="menu"] [role="menuitem"], [role="dialog"] button { background: transparent !important; color: #cbd5e1 !important; border: none !important; font-weight: 500 !important; }
        [role="menu"] button:hover, [role="menu"] [role="menuitem"]:hover, [role="dialog"] button:hover { background: rgba(0, 212, 255, 0.1) !important; color: #00d4ff !important; }
        [role="menu"] span, [role="dialog"] span, [role="menu"] label, [role="dialog"] label { color: #cbd5e1 !important; }
        [role="menu"] [role="switch"], [role="dialog"] [role="switch"] { background: rgba(0, 212, 255, 0.2) !important; }
        [role="menu"] [role="switch"][aria-checked="true"], [role="dialog"] [role="switch"][aria-checked="true"] { background: #00d4ff !important; }

        </style>
        """,
        unsafe_allow_html=True,
    )
