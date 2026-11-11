cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocked_ips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE,
        reason TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
