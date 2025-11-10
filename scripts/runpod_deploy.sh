#!/usr/bin/env bash
# Automated bootstrap and launch helper for RunPod GPU instances.

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${PROJECT_ROOT}/selenium-env"
PYTHON_BIN="${VENV_PATH}/bin/python"
PIP_BIN="${VENV_PATH}/bin/pip"

CHROME_DEB_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
CHROMEDRIVER_BASE_URL="https://storage.googleapis.com/chrome-for-testing-public"

if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
else
    SUDO=""
fi

log() {
    echo "[runpod] $*"
}

ensure_packages() {
    log "Installing system dependencies..."
    ${SUDO} apt-get update
    ${SUDO} apt-get install -y \
        python3-venv python3-pip wget curl unzip \
        libnss3 libxss1 libasound2 libxshmfence1 libgbm1 fonts-liberation \
        xdg-utils
}

ensure_chrome() {
    if command -v google-chrome >/dev/null 2>&1; then
        log "Google Chrome already installed."
        return
    fi

    log "Installing Google Chrome..."
    tmp_deb="$(mktemp --suffix=.deb)"
    wget -qO "${tmp_deb}" "${CHROME_DEB_URL}"
    ${SUDO} apt-get install -y "${tmp_deb}"
    rm -f "${tmp_deb}"
}

ensure_chromedriver() {
    if command -v chromedriver >/dev/null 2>&1; then
        log "Chromedriver already installed."
        return
    fi

    log "Installing ChromeDriver to match browser build..."
    chrome_version="$(google-chrome --version | awk '{print $3}')"
    download_url="${CHROMEDRIVER_BASE_URL}/${chrome_version}/linux64/chromedriver-linux64.zip"
    tmp_zip="$(mktemp --suffix=.zip)"

    if ! wget -qO "${tmp_zip}" "${download_url}"; then
        log "Falling back to Selenium Manager for driver resolution."
        return
    fi

    tmp_dir="$(mktemp -d)"
    unzip -q "${tmp_zip}" -d "${tmp_dir}"
    ${SUDO} mv "${tmp_dir}/chromedriver-linux64/chromedriver" /usr/local/bin/chromedriver
    ${SUDO} chmod +x /usr/local/bin/chromedriver
    rm -rf "${tmp_zip}" "${tmp_dir}"
}

ensure_venv() {
    if [[ ! -d "${VENV_PATH}" ]]; then
        log "Creating Python virtual environment..."
        python3 -m venv "${VENV_PATH}"
    fi

    log "Upgrading pip and installing Python dependencies..."
    "${PIP_BIN}" install --upgrade pip wheel
    "${PIP_BIN}" install -r "${PROJECT_ROOT}/requirements.txt"
}

start_services() {
    log "Starting Flask stream and remote control services..."
    export GPU_ENABLED="${GPU_ENABLED:-1}"
    export FRAME_RATE_SECONDS="${FRAME_RATE_SECONDS:-0.25}"
    export START_URL="${START_URL:-https://example.com}"
    export HOST="${HOST:-0.0.0.0}"

    pushd "${PROJECT_ROOT}" >/dev/null

    "${PYTHON_BIN}" flask_stream.py &
    STREAM_PID=$!

    "${PYTHON_BIN}" remote_control.py &
    API_PID=$!

    trap 'log "Shutting down..."; kill ${STREAM_PID} ${API_PID} 2>/dev/null' EXIT INT TERM
    log "Flask stream PID: ${STREAM_PID}, Remote control PID: ${API_PID}"
    wait -n "${STREAM_PID}" "${API_PID}"
}

main() {
    ensure_packages
    ensure_chrome
    ensure_chromedriver
    ensure_venv
    start_services
}

main "$@"
