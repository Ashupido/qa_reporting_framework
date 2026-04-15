# ----------------------------
# AI SUMMARY
# ----------------------------
def generate_executive_summary(metrics):
    return f"""
📊 QA EXECUTIVE SUMMARY

🔹 Status:
{format_dict(metrics.get('status_counts', {}))}

🔹 Severity:
{format_dict(metrics.get('severity_counts', {}))}

🔹 Cycles:
{format_dict(metrics.get('cycle_counts', {}))}

✔ QA analysis completed successfully.
"""


# ----------------------------
# CHATBOT
# ----------------------------
def qa_chatbot(question, metrics):
    q = question.lower()

    if "status" in q or "defect" in q:
        return format_dict(metrics.get("status_counts", {}))

    if "severity" in q:
        return format_dict(metrics.get("severity_counts", {}))

    if "cycle" in q:
        return format_dict(metrics.get("cycle_counts", {}))

    return "Ask about status, severity, or cycle data in QA."


# ----------------------------
# HELPER
# ----------------------------
def format_dict(data):
    if not data:
        return "No data available"

    return "\n".join([f"- {k}: {v}" for k, v in data.items()])