# Dev Dashboard

A lightweight, self-hosted system monitoring dashboard built with Python and Flask.
Displays real-time CPU, RAM, and disk usage alongside a live process table — all in a clean dark-themed web UI.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- Live CPU, RAM, and disk usage with color-coded indicators
- Top 10 processes by CPU usage
- Auto-refreshes every 5 seconds
- Clean dark-themed responsive UI
- Lightweight — no heavy frameworks or databases

## Tech Stack

- **Backend:** Python, Flask, psutil
- **Frontend:** HTML, CSS, Vanilla JavaScript

## Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation

1. Clone the repo
git clone https://github.com/BenLudowise/dev-dashboard.git
cd dev-dashboard

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
python app.py

5. Open your browser and go to `http://localhost:5000`

## Project Structure
dev-dashboard/
├── app.py              # Flask backend & API routes
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend dashboard
└── static/             # Static assets (future use)

## Roadmap

- [x] Flask REST API for system stats
- [x] Live-updating frontend dashboard
- [ ] Historical charts with Chart.js
- [ ] Email/desktop alerts on high usage
- [ ] Login/authentication
- [ ] One-click deployment script

## License

MIT
