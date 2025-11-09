#!/usr/bin/env python3
"""
Flask application that streams live screenshots from a headless Chrome session.

Usage:
    ./selenium-env/bin/python flask_stream.py
"""

from __future__ import annotations

import atexit
import io
import os
import time
from threading import Lock
from typing import Iterator

from flask import Flask, Response, jsonify
from PIL import Image

from selenium_worker import create_driver


FRAME_RATE_SECONDS = float(os.environ.get("FRAME_RATE_SECONDS", "0.5"))
START_URL = os.environ.get("START_URL", "https://example.com")
PROXY_URL = os.environ.get("PROXY_URL")
JPEG_QUALITY = int(os.environ.get("JPEG_QUALITY", "85"))
MAX_WIDTH = int(os.environ.get("CAPTURE_MAX_WIDTH", "1920"))
MAX_HEIGHT = int(os.environ.get("CAPTURE_MAX_HEIGHT", "1080"))


app = Flask(__name__)
_driver_lock = Lock()
_driver_context = create_driver(PROXY_URL)
_driver = _driver_context.__enter__()
_driver.get(START_URL)


@atexit.register
def _shutdown_driver():
    global _driver
    try:
        _driver_context.__exit__(None, None, None)
    finally:
        _driver = None


def _capture_frame() -> bytes:
    with _driver_lock:
        png_bytes = _driver.get_screenshot_as_png()

    image = Image.open(io.BytesIO(png_bytes))
    if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return buffer.getvalue()


def generate_frames() -> Iterator[bytes]:
    frame_interval = max(FRAME_RATE_SECONDS, 0.1)
    while True:
        frame = _capture_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )
        time.sleep(frame_interval)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/healthz")
def healthz():
    gpu_enabled = os.environ.get("GPU_ENABLED", "1")
    return jsonify(
        {
            "status": "ok",
            "start_url": START_URL,
            "frame_rate_seconds": FRAME_RATE_SECONDS,
            "jpeg_quality": JPEG_QUALITY,
            "gpu_enabled": gpu_enabled,
        }
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    app.run(host=host, port=port, debug=False)
