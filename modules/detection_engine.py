import sqlite3

DB_FILE = "database/siem.db"

def detect_brute_force(cursor):

    cursor.execute("""
    SELECT ip_address, COUNT(*)
    FROM logs
    WHERE event_type='Failed Login'
    GROUP BY ip_address
    HAVING COUNT(*) >= 5
    """)

    attackers = cursor.fetchall()

    for ip, count in attackers:

        print(f"[ALERT] Brute force detected from {ip}")

        cursor.execute("""
        INSERT INTO alerts (ip_address, alert_type, severity)
        VALUES (?, ?, ?)
        """, (ip, "Brute Force Attack", "High"))

        # Block the IP
        cursor.execute("""
        INSERT OR IGNORE INTO blocked_ips (ip_address, reason)
        VALUES (?, ?)
        """, (ip, "Brute Force Attack"))


def detect_port_scan(cursor):

    cursor.execute("""
    SELECT ip_address, COUNT(DISTINCT port)
    FROM logs
    GROUP BY ip_address
    HAVING COUNT(DISTINCT port) >= 4
    """)

    scanners = cursor.fetchall()

    for ip, count in scanners:

        print(f"[ALERT] Port scan detected from {ip}")

        cursor.execute("""
        INSERT INTO alerts (ip_address, alert_type, severity)
        VALUES (?, ?, ?)
        """, (ip, "Port Scan Detected", "Medium"))

        # Block the IP
        cursor.execute("""
        INSERT OR IGNORE INTO blocked_ips (ip_address, reason)
        VALUES (?, ?)
        """, (ip, "Port Scan Detected"))


def run_detection():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    detect_brute_force(cursor)
    detect_port_scan(cursor)

    conn.commit()
    conn.close()

    print("Detection complete!")


if __name__ == "__main__":
    run_detection()
