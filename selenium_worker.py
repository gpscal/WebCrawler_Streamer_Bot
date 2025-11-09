#!/usr/bin/env python3
"""
Headless Selenium worker with optional proxy support.

Usage:
    PROXY_URL="http://user:pass@ip:port" TARGET_URL="https://httpbin.org/ip" \
        ./selenium-env/bin/python selenium_worker.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


def _is_truthy(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() not in {"0", "false", "no", "off"}


def _gpu_available() -> bool:
    if not _is_truthy(os.environ.get("GPU_ENABLED"), default=True):
        return False

    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return False

    try:
        subprocess.run(
            [nvidia_smi],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return False

    return True


def build_options(proxy_url: str | None = None) -> Options:
    options = Options()

    headless_mode = os.environ.get("CHROME_HEADLESS", "new")
    if _is_truthy(headless_mode, default=True):
        # Allow explicit override: "legacy" or "new"
        if headless_mode.lower() in {"legacy", "old"}:
            options.add_argument("--headless")
        else:
            options.add_argument("--headless=new")

    gpu_enabled = _gpu_available()
    if gpu_enabled:
        options.add_argument("--enable-gpu")
        options.add_argument("--enable-zero-copy")
        options.add_argument("--enable-accelerated-video-decode")
        options.add_argument("--enable-features=VaapiVideoDecoder")
        options.add_argument("--use-gl=desktop")
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument("--disable-software-rasterizer")
    else:
        options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")

    chrome_binary = os.environ.get("CHROME_BINARY")
    if chrome_binary:
        options.binary_location = chrome_binary

    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")

    return options


@contextmanager
def create_driver(proxy_url: str | None = None):
    options = build_options(proxy_url)
    remote_url = os.environ.get("SELENIUM_REMOTE_URL")

    if remote_url:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    try:
        yield driver
    finally:
        driver.quit()


def run_worker(url: str, proxy_url: str | None = None) -> str:
    with create_driver(proxy_url) as driver:
        driver.get(url)
        return driver.page_source


def main(argv: list[str]) -> int:
    target_url = os.environ.get("TARGET_URL", "https://httpbin.org/ip")
    proxy_url = os.environ.get("PROXY_URL")

    try:
        html = run_worker(target_url, proxy_url)
    except WebDriverException as exc:
        sys.stderr.write(f"[selenium_worker] WebDriver error: {exc}\\n")
        return 1

    sys.stdout.write(html)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
