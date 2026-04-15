import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection

# ----------------------------
# PAGE TITLE
# ----------------------------
st.title("🐞 Defect Analytics Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM defects", conn)
conn.close()

# ----------------------------
# CHECK EMPTY DATA
# ----------------------------
if df.empty:
    st.warning("No defect data available.")
    st.stop()

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_defects = len(df)
open_defects = len(df[df["status"] == "Open"])
closed_defects = len(df[df["status"] == "Closed"])

critical = len(df[df["severity"] == "Critical"])
high = len(df[df["severity"] == "High"])
medium = len(df[df["severity"] == "Medium"])
low = len(df[df["severity"] == "Low"])

# ----------------------------
# KPI DISPLAY
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Defects", total_defects)
col2.metric("Open Defects", open_defects)
col3.metric("Closed Defects", closed_defects)
col4.metric("Critical Defects", critical)

st.markdown("---")

# ----------------------------
# DEFECT SEVERITY CHART
# ----------------------------
st.subheader("📊 Defects by Severity")

severity_data = df["severity"].value_counts().reset_index()
severity_data.columns = ["Severity", "Count"]

fig1 = px.bar(severity_data, x="Severity", y="Count", text="Count")
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# DEFECT STATUS CHART
# ----------------------------
st.subheader("📈 Defects by Status")

status_data = df["status"].value_counts().reset_index()
status_data.columns = ["Status", "Count"]

fig2 = px.pie(status_data, names="Status", values="Count")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ROOT CAUSE ANALYSIS
# ----------------------------
st.subheader("🔍 Root Cause Analysis")

root_cause_data = df["root_cause"].value_counts().reset_index()
root_cause_data.columns = ["Root Cause", "Count"]

fig3 = px.bar(root_cause_data, x="Root Cause", y="Count", text="Count")
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# DEFECT TABLE
# ----------------------------
st.subheader("📋 Defect Details")
st.dataframe(df)

# ----------------------------
# SUMMARY
# ----------------------------
st.subheader("🧠 Defect Summary")

st.write(f"""
- Total Defects: **{total_defects}**
- Open Defects: **{open_defects}**
- Closed Defects: **{closed_defects}**
- Critical: **{critical}**

👉 Focus on reducing open critical defects before release.
""")