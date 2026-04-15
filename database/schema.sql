-- =========================================
-- QA Reporting Framework Database Schema
-- =========================================

-- ----------------------------
-- 1. Test Cycles Table
-- ----------------------------
CREATE TABLE IF NOT EXISTS test_cycles (
    cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_name TEXT NOT NULL UNIQUE,
    planned_test_cases INTEGER NOT NULL,
    executed_test_cases INTEGER NOT NULL,
    passed_test_cases INTEGER NOT NULL,
    failed_test_cases INTEGER NOT NULL,
    blocked_test_cases INTEGER NOT NULL,
    deferred_test_cases INTEGER NOT NULL,
    scope_executed_pct REAL NOT NULL,
    scope_pending_pct REAL NOT NULL,
    active_flag INTEGER DEFAULT 1
);

-- ----------------------------
-- 2. Defects Table
-- ----------------------------
CREATE TABLE IF NOT EXISTS defects (
    defect_id INTEGER PRIMARY KEY AUTOINCREMENT,
    defect_title TEXT NOT NULL,
    cycle_name TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    root_cause TEXT NOT NULL,
    discovered_week TEXT NOT NULL
);

-- ----------------------------
-- 3. Alerts Table
-- ----------------------------
CREATE TABLE IF NOT EXISTS alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    priority TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);