import streamlit as st
from pathlib import Path
import importlib.util

from database.db import initialize_database
from config import APP_TITLE

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# INIT DATABASE
# ----------------------------
initialize_database()

# ----------------------------
# PATHS
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"

# ----------------------------
# SIDEBAR MENU (WITH AI ADDED)
# ----------------------------
PAGE_MAP = {
    "Executive Overview": "1_Executive_Overview.py",
    "Test Execution": "2_Test_Execution.py",
    "Defect Analytics": "3_Defect_Analytics.py",
    "Data Management": "4_Data_Management.py",
    "AI Insights Chat": "5_AI_Insights_Chat.py",  # ✅ NEW PAGE ADDED
}

st.sidebar.title("QA Reporting Framework")

selected_page = st.sidebar.radio(
    "Navigation",
    list(PAGE_MAP.keys())
)

st.sidebar.markdown("---")
st.sidebar.info("SQLite-based QA Dashboard with AI")

# ----------------------------
# SAFE PAGE LOADER
# ----------------------------
def load_page(file_name):
    file_path = PAGES_DIR / file_name

    if not file_path.exists():
        st.error(f"Page not found: {file_name}")
        return None

    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ----------------------------
# RUN PAGE
# ----------------------------
page_file = PAGE_MAP[selected_page]
load_page(page_file)