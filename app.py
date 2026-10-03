import os
import time
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

MEXC_BASE = "https://api.mexc.com"
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "").strip()

VALID_INTERVALS = {"Min1","Min5","Min15","Min30","Min60","Hour4","Hour8","Day1","Week1","Month1"}

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "service": "Carteira Micro EGI 3x V3",
        "time": int(time.time()),
        "ntfy_configured": bool(NTFY_TOPIC),
    })

@app.get("/api/kline/<symbol>")
def kline(symbol):
    symbol = symbol.upper().replace("/", "_").replace("-", "_")
    interval = request.args.get("interval", "Min15")
    if interval not in VALID_INTERVALS:
        return jsonify({"ok": False, "error": "intervalo inválido"}), 400

    try:
        limit = max(60, min(int(request.args.get("limit", "180")), 500))
    except ValueError:
        limit = 180

    seconds = {
        "Min1":60,"Min5":300,"Min15":900,"Min30":1800,"Min60":3600,
        "Hour4":14400,"Hour8":28800,"Day1":86400,"Week1":604800,"Month1":2592000
    }[interval]

    end = int(time.time())
    start = end - seconds * (limit + 8)

    url = f"{MEXC_BASE}/api/v1/contract/kline/{symbol}"
    try:
        r = requests.get(
            url,
            params={"interval": interval, "start": start, "end": end},
            timeout=12,
            headers={"User-Agent": "Carteira-Micro-EGI/3.0"}
        )
        r.raise_for_status()
        payload = r.json()
        if not payload.get("success"):
            return jsonify({
                "ok": False,
                "error": payload.get("message") or "MEXC retornou falha",
                "mexc": payload
            }), 502

        return jsonify({"ok": True, "source": "MEXC Futures", "data": payload["data"]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502

@app.post("/api/ntfy")
def ntfy():
    body = request.get_json(silent=True) or {}
    topic = (body.get("topic") or NTFY_TOPIC or "").strip()
    if not topic:
        return jsonify({"ok": False, "error": "NTFY_TOPIC não configurado"}), 400

    # Mantém somente caracteres simples no tópico
    topic = "".join(ch for ch in topic if ch.isalnum() or ch in "-_")
    if not topic:
        return jsonify({"ok": False, "error": "tópico inválido"}), 400

    title = str(body.get("title") or "Carteira Micro EGI 3x")[:200]
    message = str(body.get("message") or "")[:4000]
    priority = str(body.get("priority") or "4")
    tags = str(body.get("tags") or "chart_with_upwards_trend,warning")[:300]

    try:
        r = requests.post(
            f"{NTFY_SERVER}/{topic}",
            data=message.encode("utf-8"),
            headers={"Title": title, "Priority": priority, "Tags": tags},
            timeout=12
        )
        r.raise_for_status()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502
