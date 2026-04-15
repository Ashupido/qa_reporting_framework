import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection

# ----------------------------
# PAGE TITLE
# ----------------------------
st.title("📂 Test Execution Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM test_cycles", conn)
conn.close()

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_planned = df["planned_test_cases"].sum()
total_executed = df["executed_test_cases"].sum()
total_passed = df["passed_test_cases"].sum()
total_failed = df["failed_test_cases"].sum()

execution_rate = round((total_executed / total_planned) * 100, 2) if total_planned > 0 else 0
pass_rate = round((total_passed / total_executed) * 100, 2) if total_executed > 0 else 0

# ----------------------------
# KPI DISPLAY
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Execution Rate %", execution_rate)
col2.metric("Pass Rate %", pass_rate)
col3.metric("Total Executed", total_executed)

st.markdown("---")

# ----------------------------
# TABLE VIEW
# ----------------------------
st.subheader("📊 Test Cycle Details")
st.dataframe(df)

# ----------------------------
# EXECUTION CHART
# ----------------------------
st.subheader("📈 Execution vs Planned")

chart_data = df[["cycle_name", "planned_test_cases", "executed_test_cases"]]

fig = px.bar(
    chart_data,
    x="cycle_name",
    y=["planned_test_cases", "executed_test_cases"],
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# SUMMARY
# ----------------------------
st.subheader("🧠 Execution Summary")

st.write(f"""
- Total Planned: **{total_planned}**
- Total Executed: **{total_executed}**
- Execution Rate: **{execution_rate}%**
- Pass Rate: **{pass_rate}%**

👉 This shows how much of the QA scope was actually completed.
""")