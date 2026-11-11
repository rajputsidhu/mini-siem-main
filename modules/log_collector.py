import sqlite3

LOG_FILE = "logs/sample_logs.txt"
DB_FILE = "database/siem.db"

def parse_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Split line into components
            try:
                event_type, ip_address, port = line.split(",")
            except ValueError:
                print(f"Skipping invalid log format: {line}")
                continue

            # Insert into database
            cursor.execute("""
                INSERT INTO logs (event_type, ip_address, port)
                VALUES (?, ?, ?)
            """, (event_type.strip(), ip_address.strip(), int(port.strip())))

    conn.commit()
    conn.close()

    print("Logs inserted successfully!")

if __name__ == "__main__":
    parse_logs()
