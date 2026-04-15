import sqlite3
from pathlib import Path

# ----------------------------
# DB PATH
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "qa_reporting.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# METRICS FUNCTION
# ----------------------------
def get_defect_analytics_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    # Status
    cursor.execute("SELECT status, COUNT(*) FROM defects GROUP BY status")
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Severity
    cursor.execute("SELECT severity, COUNT(*) FROM defects GROUP BY severity")
    severity_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Cycle
    cursor.execute("SELECT cycle_name, COUNT(*) FROM defects GROUP BY cycle_name")
    cycle_counts = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    return {
        "status_counts": status_counts,
        "severity_counts": severity_counts,
        "cycle_counts": cycle_counts
    }