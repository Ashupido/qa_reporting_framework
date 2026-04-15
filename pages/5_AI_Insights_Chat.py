import streamlit as st
import sys
from pathlib import Path

# ----------------------------
# PATH FIX
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import services.metrics_service as metrics_service
import services.openai_service as ai_service

st.set_page_config(page_title="AI QA Insights", layout="wide")

st.title("🤖 AI QA Insights & Chatbot")

# ----------------------------
# LOAD DATA
# ----------------------------
metrics = metrics_service.get_defect_analytics_metrics()

# ----------------------------
# EXECUTIVE SUMMARY
# ----------------------------
st.header("📊 AI Executive Summary")

if st.button("Generate AI Summary"):
    summary = ai_service.generate_executive_summary(metrics)
    st.success("AI Summary Generated")
    st.write(summary)

st.divider()

# ----------------------------
# METRICS DISPLAY (CLEAN UI)
# ----------------------------
st.header("📊 QA Metrics Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Status Counts")
    st.json(metrics["status_counts"])

with col2:
    st.subheader("Severity Counts")
    st.json(metrics["severity_counts"])

with col3:
    st.subheader("Cycle Counts")
    st.json(metrics["cycle_counts"])

# CHATBOT UI (CLEAN)
# ----------------------------
st.header("💬 QA Chatbot")

question = st.text_input("Ask a QA question:")

if st.button("Ask AI"):
    if question.strip():
        answer = ai_service.qa_chatbot(question, metrics)
        st.success("Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question")