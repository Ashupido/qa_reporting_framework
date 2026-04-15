import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection

# ----------------------------
# PAGE TITLE
# ----------------------------
st.title("📊 QA Executive Overview")

# ----------------------------
# LOAD DATA FROM DB
# ----------------------------
conn = get_connection()

test_cycles = pd.read_sql_query("SELECT * FROM test_cycles", conn)
defects = pd.read_sql_query("SELECT * FROM defects", conn)

conn.close()

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_tests = test_cycles["planned_test_cases"].sum()
executed = test_cycles["executed_test_cases"].sum()
passed = test_cycles["passed_test_cases"].sum()
failed = test_cycles["failed_test_cases"].sum()

pass_rate = round((passed / executed) * 100, 2) if executed > 0 else 0

total_defects = len(defects)
high_severity = len(defects[defects["severity"] == "High"])
critical_defects = len(defects[defects["severity"] == "Critical"])

# ----------------------------
# KPI DISPLAY
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Test Cases", total_tests)
col2.metric("Executed", executed)
col3.metric("Pass Rate %", pass_rate)
col4.metric("Total Defects", total_defects)

st.markdown("---")

# ----------------------------
# DEFECT SEVERITY CHART
# ----------------------------
st.subheader("🐞 Defects by Severity")

severity_data = defects["severity"].value_counts().reset_index()
severity_data.columns = ["Severity", "Count"]

fig = px.bar(severity_data, x="Severity", y="Count", text="Count")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# TEST EXECUTION PIE CHART
# ----------------------------
st.subheader("📈 Test Execution Summary")

exec_data = pd.DataFrame({
    "Status": ["Passed", "Failed"],
    "Count": [passed, failed]
})

fig2 = px.pie(exec_data, names="Status", values="Count")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# QA SUMMARY
# ----------------------------
st.subheader("🧠 QA Summary")

st.write(f"""
- **Pass Rate:** {pass_rate}%
- **Total Defects:** {total_defects}
- **High Severity Defects:** {high_severity}
- **Critical Defects:** {critical_defects}

👉 This overview gives a quick snapshot of release quality.
""")