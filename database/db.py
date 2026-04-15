import sqlite3
from pathlib import Path
from config import DATABASE_PATH

# Get base directory
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / DATABASE_PATH


# ----------------------------
# CONNECT TO DATABASE
# ----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# INITIALIZE DATABASE
# ----------------------------
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Read schema file
    schema_path = BASE_DIR / "database" / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Execute schema
    cursor.executescript(schema_sql)

    conn.commit()
    conn.close()

    # Load sample data if tables are empty
    insert_sample_data()


# ----------------------------
# SAMPLE DATA
# ----------------------------
def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM test_cycles")
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return  # already has data

    # ---------------- TEST CYCLES ----------------
    cursor.execute("""
        INSERT INTO test_cycles (
            cycle_name, planned_test_cases, executed_test_cases,
            passed_test_cases, failed_test_cases, blocked_test_cases,
            deferred_test_cases, scope_executed_pct, scope_pending_pct
        )
        VALUES
        ('Sprint 1 Regression', 100, 90, 80, 10, 2, 8, 90.0, 10.0),
        ('UAT Cycle', 120, 110, 95, 10, 3, 7, 91.6, 8.4)
    """)

    # ---------------- DEFECTS ----------------
    cursor.execute("""
        INSERT INTO defects (
            defect_title, cycle_name, severity, status,
            root_cause, discovered_week
        )
        VALUES
        ('Login failure issue', 'Sprint 1 Regression', 'High', 'Open', 'Code Bug', 'Week 1'),
        ('UI misalignment', 'UAT Cycle', 'Low', 'Closed', 'UI Issue', 'Week 2'),
        ('Payment gateway timeout', 'Sprint 1 Regression', 'Critical', 'Open', 'API Failure', 'Week 1')
    """)

    # ---------------- ALERTS ----------------
    cursor.execute("""
        INSERT INTO alerts (message, priority)
        VALUES
        ('Pass rate below threshold', 'High'),
        ('High severity defects detected', 'Critical')
    """)

    conn.commit()
    conn.close()