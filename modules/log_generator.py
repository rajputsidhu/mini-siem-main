import sqlite3
import random
import time

DB_FILE = "database/siem.db"

IPS = [
"192.168.1.10",
"192.168.1.20",
"192.168.1.30",
"10.0.0.5",
"172.16.0.8"
]

PORTS = [21,22,23,25,53,80,110,143,443,3306,8080]

def generate_logs():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    attack_type = random.choice([
        "normal",
        "ssh_bruteforce",
        "port_scan",
        "web_scan"
    ])

    ip = random.choice(IPS)

    if attack_type == "normal":

        event = random.choice(["Successful Login","Failed Login"])
        port = random.choice(PORTS)

        cursor.execute("""
        INSERT INTO logs (event_type, ip_address, port)
        VALUES (?,?,?)
        """,(event,ip,port))


    elif attack_type == "ssh_bruteforce":

        for i in range(random.randint(4,8)):

            cursor.execute("""
            INSERT INTO logs (event_type, ip_address, port)
            VALUES (?,?,?)
            """,("Failed Login",ip,22))


    elif attack_type == "port_scan":

        scan_ports = random.sample(PORTS,5)

        for port in scan_ports:

            cursor.execute("""
            INSERT INTO logs (event_type, ip_address, port)
            VALUES (?,?,?)
            """,("Connection Attempt",ip,port))


    elif attack_type == "web_scan":

        for i in range(random.randint(3,6)):

            cursor.execute("""
            INSERT INTO logs (event_type, ip_address, port)
            VALUES (?,?,?)
            """,("Connection Attempt",ip,80))


    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_logs()
