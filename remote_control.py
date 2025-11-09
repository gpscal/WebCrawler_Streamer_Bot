#!/usr/bin/env python3
"""
Minimal remote control API that triggers a Selenium run on demand.

Usage:
    ./selenium-env/bin/python remote_control.py
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from selenium_worker import run_worker


DEFAULT_TARGET = "https://httpbin.org/ip"


app = Flask(__name__)


@app.route("/run", methods=["POST", "GET"])
def run():
    payload = request.get_json(silent=True) or {}
    target_url = payload.get("target_url") or request.args.get("target_url") or DEFAULT_TARGET
    proxy_url = payload.get("proxy_url") or request.args.get("proxy_url") or os.environ.get("PROXY_URL")

    html = run_worker(target_url, proxy_url)

    return jsonify(
        {
            "status": "Task executed successfully",
            "target_url": target_url,
            "proxy_url": proxy_url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload_preview": html[:500],
        }
    )


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=False)
