#!/usr/bin/env bash
# Quick start script for the enhanced Flask stream service

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_ROOT}"

# Set environment variables
export GPU_ENABLED="${GPU_ENABLED:-1}"
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8000}"
export FRAME_RATE_SECONDS="${FRAME_RATE_SECONDS:-0.25}"
export START_URL="${START_URL:-https://example.com}"

echo "Starting enhanced Flask stream service..."
echo "GPU_ENABLED: ${GPU_ENABLED}"
echo "HOST: ${HOST}"
echo "PORT: ${PORT}"
echo "FRAME_RATE_SECONDS: ${FRAME_RATE_SECONDS}"
echo "START_URL: ${START_URL}"

# Start the service
nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &
PID=$!

echo "Service started with PID: ${PID}"
echo "Logs: tail -f flask_stream_enhanced.log"
echo "Stop with: kill ${PID}"

# Save PID for easy stopping
echo "${PID}" > flask_stream_enhanced.pid
