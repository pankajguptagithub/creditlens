import sqlite3

from app.core.config import load_config

def create_audit_table():
    config = load_config()
    database_path = config["audit_database_path"]

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS risk_audit(
            request_id TEXT PRIMARY KEY,
            timestamp TEXT,
            customer_id TEXT,
            default_probability REAL,
            risk_band TEXT
        )
        """
    )

    connection.commit()
    connection.close()

def save_audit_record(audit_record):
    config = load_config()
    database_path = config["audit_database_path"]

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO risk_audit(
            request_id,
            timestamp,
            customer_id,
            default_probability,
            risk_band
        )
        VALUES (?,?,?,?,?)
        """,
        (
            audit_record["request_id"],
            audit_record["timestamp"],
            audit_record["customer_id"],
            audit_record["default_probability"],
            audit_record["risk_band"],
        )
    )

    connection.commit()
    connection.close()

def load_audit_records():
    config = load_config()
    database_path = config["audit_database_path"]

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 
            request_id,
            timestamp,
            customer_id,
            default_probability,
            risk_band
        FROM risk_audit
        ORDER BY timestamp DESC
        """
    )

    rows = cursor.fetchall()
    connection.close()

    records = []

    for row in rows:
        records.append({
            "request_id": row[0],
            "timestamp": row[1],
            "customer_id": row[2],
            "default_probability": row[3],
            "risk_band": row[4],

        })

    return records
