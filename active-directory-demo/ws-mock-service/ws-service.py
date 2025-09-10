from flask import Flask, request, jsonify
from flask_sock import Sock
import os

app = Flask(__name__)
sock = Sock(app)
port = int(os.getenv("PORT", "5000"))

@sock.route('/ws')
def notify(ws):
    while True:
        msg = ws.receive()
        if msg is None:  # connection closed
            break
        print(f"[WS] Notification: {msg}", flush=True)
        ws.send(f"ACK: {msg}")

def start(args=None, hkube_api=None):
    """HKube entrypoint – starts the service."""
    print(f"Starting service on port {port}...")
    # Flask will block here, so process stays alive
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()

