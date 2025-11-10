#!/bin/bash
# Quick status check script for WebCrawler Streamer Bot

echo "=========================================="
echo "WebCrawler Streamer Bot - Status Check"
echo "=========================================="
echo ""

# Check if services are running
echo "📊 Service Status:"
echo "------------------"
if pgrep -f "flask_stream.py" > /dev/null; then
    STREAM_PID=$(pgrep -f "flask_stream.py")
    echo "✅ Flask Stream: Running (PID: $STREAM_PID)"
else
    echo "❌ Flask Stream: Not Running"
fi

if pgrep -f "remote_control.py" > /dev/null; then
    CONTROL_PID=$(pgrep -f "remote_control.py")
    echo "✅ Remote Control: Running (PID: $CONTROL_PID)"
else
    echo "❌ Remote Control: Not Running"
fi

echo ""

# Check ports
echo "🔌 Port Status:"
echo "---------------"
if ss -tlnp | grep -q ":8000"; then
    echo "✅ Port 8000 (Flask Stream): Listening"
else
    echo "❌ Port 8000 (Flask Stream): Not Listening"
fi

if ss -tlnp | grep -q ":5000"; then
    echo "✅ Port 5000 (Remote Control): Listening"
else
    echo "❌ Port 5000 (Remote Control): Not Listening"
fi

echo ""

# GPU Status
echo "🎮 GPU Status:"
echo "--------------"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | \
    awk -F', ' '{printf "GPU: %s\nMemory: %s MB / %s MB\nUtilization: %s%%\n", $1, $2, $3, $4}'
else
    echo "❌ nvidia-smi not found"
fi

echo ""

# Test Health Endpoints
echo "🏥 Health Check:"
echo "----------------"
if curl -s --max-time 5 http://localhost:8000/healthz > /dev/null 2>&1; then
    echo "✅ Flask Stream Health: OK"
    curl -s http://localhost:8000/healthz | python3 -m json.tool 2>/dev/null || echo ""
else
    echo "❌ Flask Stream Health: Failed"
fi

echo ""

if curl -s --max-time 5 http://localhost:5000/healthz > /dev/null 2>&1; then
    echo "✅ Remote Control Health: OK"
else
    echo "❌ Remote Control Health: Failed"
fi

echo ""

# RunPod Info
echo "🌐 RunPod Information:"
echo "---------------------"
echo "Pod ID: ${RUNPOD_POD_ID:-Not Set}"
echo "Public IP: ${RUNPOD_PUBLIC_IP:-Not Set}"
echo "Data Center: ${RUNPOD_DC_ID:-Not Set}"
echo ""
echo "Public Access URLs:"
if [ -n "$RUNPOD_PUBLIC_IP" ] && [ -n "$RUNPOD_TCP_PORT_8000" ]; then
    echo "  Video Stream: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_8000}/video_feed"
    echo "  Remote API:   http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_5000}/run"
else
    echo "  ⚠️  RunPod environment variables not found"
fi

echo ""
echo "=========================================="
echo "Status check complete!"
echo "=========================================="
