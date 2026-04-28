# Secure File Explorer

A simple and secure web-based file explorer built with Flask.

## Features

- Modern dark UI
- Login authentication
- Browse folders and download files
- Download entire folder as ZIP
- Restricted to allowed paths only

## Installation

1. Clone or download the project.
2. Install dependencies:
```bash
pip install flask
```

## How to Run

### Setup
- Place `app.py` in your desired directory.
- Run the application:
```bash
python app.py
```
- On first run, enter your desired username and password in the terminal.
- Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Default Access
- **First time:** You will set username and password during startup.
- **Allowed paths:** `~/Downloads`, `D:\`, `E:\` (you can modify in code).

## Login
Use the credentials you set when starting the app.

## Notes
- Run with `debug=True` (development only).
- Access from other devices using your local IP (shown in terminal).
- Press `Ctrl + C` to stop the server.
