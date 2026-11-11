import sqlite3

DB_FILE = "database/siem.db"

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            ip_address TEXT,
            port INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            alert_type TEXT,
            severity TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Blocked IPs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully")


if __name__ == "__main__":
    create_database()
