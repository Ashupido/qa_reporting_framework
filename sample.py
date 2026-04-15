import sqlite3
from database.db import get_connection


# ----------------------------
# CHECK IF TABLE IS EMPTY
# ----------------------------
def check_if_table_empty(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count == 0


# ----------------------------
# INSERT TEST CYCLES
# ----------------------------
def insert_sample_test_cycles(conn):
    cursor = conn.cursor()

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

    conn.commit()


# ----------------------------
# INSERT DEFECTS
# ----------------------------
def insert_sample_defects(conn):
    cursor = conn.cursor()

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

    conn.commit()


# ----------------------------
# INSERT ALERTS
# ----------------------------
def insert_sample_alerts(conn):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (message, priority, is_active)
        VALUES
        ('Pass rate dropped below 90% in Sprint 1 Regression', 'High', 1),
        ('High defect count found in UAT Cycle', 'High', 1),
        ('Coverage low in Reports module', 'Medium', 1),
        ('No critical defects closed this week', 'Low', 1)
    """)

    conn.commit()


# ----------------------------
# MAIN RUNNER
# ----------------------------
def main():
    conn = get_connection()

    if check_if_table_empty(conn, "test_cycles"):
        print("Inserting test_cycles...")
        insert_sample_test_cycles(conn)

    if check_if_table_empty(conn, "defects"):
        print("Inserting defects...")
        insert_sample_defects(conn)

    if check_if_table_empty(conn, "alerts"):
        print("Inserting alerts...")
        insert_sample_alerts(conn)

    conn.close()
    print("Sample data loaded successfully.")


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    main()