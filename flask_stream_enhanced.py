#!/usr/bin/env python3
"""
Enhanced Flask application that streams live screenshots with human-like behavior.
Includes automatic scrolling and next page navigation.

Usage:
    ./selenium-env/bin/python flask_stream_enhanced.py
"""

from __future__ import annotations

import atexit
import io
import os
import time
import threading
from threading import Lock, Event
from typing import Iterator, Optional

from flask import Flask, Response, jsonify, request
from PIL import Image

from selenium_worker import create_driver
from human_behavior import HumanBehavior


FRAME_RATE_SECONDS = float(os.environ.get("FRAME_RATE_SECONDS", "0.5"))
START_URL = os.environ.get("START_URL", "https://example.com")
PROXY_URL = os.environ.get("PROXY_URL")
JPEG_QUALITY = int(os.environ.get("JPEG_QUALITY", "85"))
MAX_WIDTH = int(os.environ.get("CAPTURE_MAX_WIDTH", "1920"))
MAX_HEIGHT = int(os.environ.get("CAPTURE_MAX_HEIGHT", "1080"))
AUTO_SCROLL = os.environ.get("AUTO_SCROLL", "1") == "1"
AUTO_NEXT = os.environ.get("AUTO_NEXT", "1") == "1"
SCROLL_INTERVAL = float(os.environ.get("SCROLL_INTERVAL", "10.0"))  # Time between auto-scrolls


app = Flask(__name__)
_driver_lock = Lock()
_driver_context = create_driver(PROXY_URL)
_driver = _driver_context.__enter__()
_human = HumanBehavior(_driver)
_driver.get(START_URL)

# State management
_state = {
    "current_url": START_URL,
    "auto_scroll_enabled": AUTO_SCROLL,
    "auto_next_enabled": AUTO_NEXT,
    "is_scrolling": False,
    "last_action": "initialized",
    "page_count": 1,
}
_state_lock = Lock()
_stop_event = Event()


@atexit.register
def _shutdown_driver():
    global _driver
    try:
        _stop_event.set()
        _driver_context.__exit__(None, None, None)
    finally:
        _driver = None


def _auto_scroll_worker():
    """Background worker that periodically scrolls the page."""
    while not _stop_event.is_set():
        try:
            time.sleep(SCROLL_INTERVAL)
            
            with _state_lock:
                if not _state["auto_scroll_enabled"] or _state["is_scrolling"]:
                    continue
                _state["is_scrolling"] = True
                _state["last_action"] = "auto_scrolling"
            
            with _driver_lock:
                # Scroll down slowly (3-5 scrolls)
                _human.scroll_down_slowly(
                    scroll_pause_time=1.5,
                    num_scrolls=random.randint(3, 5),
                    scroll_percentage=0.3,
                )
                
                # Try to find and click next page if enabled
                with _state_lock:
                    if _state["auto_next_enabled"]:
                        next_button = _human.find_next_page_button()
                        if next_button:
                            _state["last_action"] = "clicking_next_page"
                            _human.human_click(next_button)
                            time.sleep(2)  # Wait for page load
                            _state["current_url"] = _driver.current_url
                            _state["page_count"] += 1
                            _state["last_action"] = f"loaded_page_{_state['page_count']}"
            
            with _state_lock:
                _state["is_scrolling"] = False
                if _state["last_action"].startswith("auto_scrolling"):
                    _state["last_action"] = "idle"
                    
        except Exception as e:
            print(f"Auto-scroll worker error: {e}")
            with _state_lock:
                _state["is_scrolling"] = False


# Start auto-scroll worker thread
if AUTO_SCROLL:
    import random
    _scroll_thread = threading.Thread(target=_auto_scroll_worker, daemon=True)
    _scroll_thread.start()


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
    with _state_lock:
        state_copy = _state.copy()
    
    gpu_enabled = os.environ.get("GPU_ENABLED", "1")
    return jsonify(
        {
            "status": "ok",
            "start_url": START_URL,
            "current_url": state_copy["current_url"],
            "frame_rate_seconds": FRAME_RATE_SECONDS,
            "jpeg_quality": JPEG_QUALITY,
            "gpu_enabled": gpu_enabled,
            "auto_scroll_enabled": state_copy["auto_scroll_enabled"],
            "auto_next_enabled": state_copy["auto_next_enabled"],
            "last_action": state_copy["last_action"],
            "page_count": state_copy["page_count"],
            "is_scrolling": state_copy["is_scrolling"],
        }
    )


@app.route("/navigate", methods=["POST"])
def navigate():
    """Navigate to a new URL with human-like behavior."""
    data = request.get_json() or {}
    url = data.get("url")
    scroll = data.get("scroll", True)
    find_next = data.get("find_next", True)
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        with _driver_lock:
            result = _human.navigate_and_scroll(url, scroll_count=None if scroll else 0, find_next=find_next)
        
        with _state_lock:
            _state["current_url"] = _driver.current_url
            if result.get("next_page_clicked"):
                _state["page_count"] += 1
            _state["last_action"] = "manual_navigation"
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/scroll", methods=["POST"])
def scroll():
    """Manually trigger scrolling."""
    data = request.get_json() or {}
    num_scrolls = data.get("num_scrolls", 5)
    
    try:
        with _state_lock:
            _state["is_scrolling"] = True
            _state["last_action"] = "manual_scrolling"
        
        with _driver_lock:
            _human.scroll_down_slowly(
                scroll_pause_time=1.5,
                num_scrolls=num_scrolls,
                scroll_percentage=0.3,
            )
        
        with _state_lock:
            _state["is_scrolling"] = False
            _state["last_action"] = "idle"
        
        return jsonify({"success": True, "scrolls_performed": num_scrolls})
    except Exception as e:
        with _state_lock:
            _state["is_scrolling"] = False
        return jsonify({"error": str(e)}), 500


@app.route("/next_page", methods=["POST"])
def next_page():
    """Find and click the next page button."""
    try:
        with _driver_lock:
            next_button = _human.find_next_page_button()
            
            if not next_button:
                return jsonify({"success": False, "error": "Next page button not found"})
            
            _human.human_click(next_button)
            time.sleep(2)  # Wait for page load
            
            new_url = _driver.current_url
        
        with _state_lock:
            _state["current_url"] = new_url
            _state["page_count"] += 1
            _state["last_action"] = f"loaded_page_{_state['page_count']}"
        
        return jsonify({
            "success": True,
            "new_url": new_url,
            "page_count": _state["page_count"],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/config", methods=["GET", "POST"])
def config():
    """Get or update configuration."""
    if request.method == "GET":
        with _state_lock:
            return jsonify({
                "auto_scroll_enabled": _state["auto_scroll_enabled"],
                "auto_next_enabled": _state["auto_next_enabled"],
                "scroll_interval": SCROLL_INTERVAL,
            })
    
    # POST - update config
    data = request.get_json() or {}
    
    with _state_lock:
        if "auto_scroll_enabled" in data:
            _state["auto_scroll_enabled"] = bool(data["auto_scroll_enabled"])
        if "auto_next_enabled" in data:
            _state["auto_next_enabled"] = bool(data["auto_next_enabled"])
    
    return jsonify({"success": True, "config": _state})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    app.run(host=host, port=port, debug=False, threaded=True)
