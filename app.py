from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

from modules.log_generator import generate_logs
from modules.detection_engine import run_detection

app = Flask(__name__)
app.secret_key = "mini_siem_secret"

DB_FILE = "database/siem.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Generate simulated logs
    generate_logs()

    # Run detection engine
    run_detection()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Logs
    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    logs = cursor.fetchall()

    # Alerts
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 50")
    alerts = cursor.fetchall()

    # Blocked IPs
    cursor.execute("SELECT * FROM blocked_ips ORDER BY id DESC")
    blocked_ips = cursor.fetchall()

    # Statistics
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE event_type='Failed Login'")
    failed_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE event_type='Successful Login'")
    success_count = cursor.fetchone()[0]

    # Threat Level
    if total_alerts < 5:
        threat_level = "LOW"
    elif total_alerts < 15:
        threat_level = "MEDIUM"
    else:
        threat_level = "HIGH"

    # Top attacking IPs
    cursor.execute("""
        SELECT ip_address, COUNT(*) as count
        FROM logs
        GROUP BY ip_address
        ORDER BY count DESC
        LIMIT 5
    """)
    top_ips = cursor.fetchall()

    # Most targeted ports
    cursor.execute("""
        SELECT port, COUNT(*) as count
        FROM logs
        GROUP BY port
        ORDER BY count DESC
        LIMIT 5
    """)
    top_ports = cursor.fetchall()

    # Recent alerts for live feed
    cursor.execute("""
        SELECT alert_type, ip_address, timestamp
        FROM alerts
        ORDER BY id DESC
        LIMIT 10
    """)
    recent_alerts = cursor.fetchall()

    # Attack Intelligence

    # Top attacker
    cursor.execute("""
        SELECT ip_address, COUNT(*) as count
        FROM logs
        GROUP BY ip_address
        ORDER BY count DESC
        LIMIT 1
    """)
    top_attacker = cursor.fetchone()

    if top_attacker:
        top_attacker_ip = top_attacker[0]
    else:
        top_attacker_ip = "None"

    # Most targeted port
    cursor.execute("""
        SELECT port, COUNT(*) as count
        FROM logs
        GROUP BY port
        ORDER BY count DESC
        LIMIT 1
    """)
    top_port = cursor.fetchone()

    if top_port:
        top_port_value = top_port[0]
    else:
        top_port_value = "None"

    # Blocked attackers count
    cursor.execute("SELECT COUNT(*) FROM blocked_ips")
    blocked_count = cursor.fetchone()[0]

    # Attack frequency (last minute)
    cursor.execute("""
        SELECT COUNT(*)
        FROM logs
        WHERE timestamp >= datetime('now','-1 minute')
    """)
    attack_frequency = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        logs=logs,
        alerts=alerts,
        blocked_ips=blocked_ips,
        total_logs=total_logs,
        total_alerts=total_alerts,
        failed_count=failed_count,
        success_count=success_count,
        top_ips=top_ips,
        top_ports=top_ports,
        recent_alerts=recent_alerts,
        threat_level=threat_level,
        top_attacker_ip=top_attacker_ip,
        top_port_value=top_port_value,
        blocked_count=blocked_count,
        attack_frequency=attack_frequency
    )


if __name__ == "__main__":
    app.run(debug=True)
