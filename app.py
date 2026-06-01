from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
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
    app.run(debug=True, host='0.0.0.0', port=5000)