from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from plyer import notification
import psutil
import threading
import time
import os

app = Flask(__name__)
app.secret_key = 'change-this-to-something-random'

# Login credentials — change these!
USERNAME = 'admin'
PASSWORD = 'password123'

# Alert thresholds
CPU_THRESHOLD = 85
RAM_THRESHOLD = 85

def send_alert(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Dev Dashboard",
        timeout=5
    )

def monitor_alerts():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if cpu > CPU_THRESHOLD:
            send_alert(
                "⚠️ High CPU Usage",
                f"CPU is at {cpu}% — above {CPU_THRESHOLD}% threshold"
            )

        if ram > RAM_THRESHOLD:
            send_alert(
                "⚠️ High RAM Usage",
                f"RAM is at {ram}% — above {RAM_THRESHOLD}% threshold"
            )

        time.sleep(30)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/stats')
@login_required
def get_stats():
    stats = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('C:\\').total,
            "used": psutil.disk_usage('C:\\').used,
            "percent": psutil.disk_usage('C:\\').percent
        },
        "uptime": psutil.boot_time()
    }
    return jsonify(stats)

@app.route('/api/processes')
@login_required
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            pass

    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]
    return jsonify(processes)

if __name__ == '__main__':
    alert_thread = threading.Thread(target=monitor_alerts, daemon=True)
    alert_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)