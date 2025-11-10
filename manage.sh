#!/bin/bash
# Management script for WebCrawler Streamer Bot

PROJECT_ROOT="/WebCrawler_Streamer_Bot"
cd "$PROJECT_ROOT"

case "$1" in
    start)
        echo "Starting WebCrawler Streamer Bot services..."
        
        # Start Flask Stream
        GPU_ENABLED=1 START_URL="${START_URL:-https://example.com}" \
        FRAME_RATE_SECONDS="${FRAME_RATE_SECONDS:-0.5}" \
        HOST=0.0.0.0 PORT=8000 \
        nohup ./selenium-env/bin/python flask_stream.py > flask_stream.log 2>&1 &
        
        echo "Started Flask Stream (PID: $!)"
        
        # Wait a moment
        sleep 2
        
        # Start Remote Control
        HOST=0.0.0.0 PORT=5000 \
        nohup ./selenium-env/bin/python remote_control.py > remote_control.log 2>&1 &
        
        echo "Started Remote Control (PID: $!)"
        echo ""
        echo "Services started! Run './manage.sh status' to check."
        ;;
        
    stop)
        echo "Stopping WebCrawler Streamer Bot services..."
        pkill -f flask_stream.py && echo "Stopped Flask Stream" || echo "Flask Stream not running"
        pkill -f remote_control.py && echo "Stopped Remote Control" || echo "Remote Control not running"
        ;;
        
    restart)
        echo "Restarting WebCrawler Streamer Bot services..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        ./check_status.sh
        ;;
        
    logs)
        if [ "$2" == "stream" ]; then
            echo "=== Flask Stream Logs (last 50 lines) ==="
            tail -50 flask_stream.log
        elif [ "$2" == "api" ] || [ "$2" == "control" ]; then
            echo "=== Remote Control Logs (last 50 lines) ==="
            tail -50 remote_control.log
        else
            echo "=== Flask Stream Logs ==="
            tail -20 flask_stream.log
            echo ""
            echo "=== Remote Control Logs ==="
            tail -20 remote_control.log
            echo ""
            echo "Use './manage.sh logs stream' or './manage.sh logs api' for full logs"
        fi
        ;;
        
    tail)
        if [ "$2" == "stream" ]; then
            tail -f flask_stream.log
        elif [ "$2" == "api" ] || [ "$2" == "control" ]; then
            tail -f remote_control.log
        else
            echo "Usage: ./manage.sh tail [stream|api]"
            echo "  stream  - Follow Flask Stream logs"
            echo "  api     - Follow Remote Control logs"
        fi
        ;;
        
    test)
        echo "Testing WebCrawler Streamer Bot..."
        echo ""
        
        echo "1. Testing Flask Stream health..."
        curl -s http://localhost:8000/healthz | python3 -m json.tool 2>/dev/null || echo "Failed"
        echo ""
        
        echo "2. Testing Remote Control health..."
        curl -s http://localhost:5000/healthz | python3 -m json.tool 2>/dev/null || echo "Failed"
        echo ""
        
        echo "3. Testing web crawling (httpbin.org/ip)..."
        curl -s "http://localhost:5000/run?target_url=https://httpbin.org/ip" | python3 -m json.tool 2>/dev/null || echo "Failed"
        echo ""
        
        echo "Tests complete!"
        ;;
        
    urls)
        echo "=== WebCrawler Streamer Bot URLs ==="
        echo ""
        if [ -n "$RUNPOD_PUBLIC_IP" ]; then
            echo "🌍 PUBLIC ACCESS (from anywhere):"
            echo "  Video Stream: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_8000}/video_feed"
            echo "  Stream Health: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_8000}/healthz"
            echo "  Remote API: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_5000}/run"
            echo "  API Health: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_5000}/healthz"
        else
            echo "⚠️  RunPod environment variables not found"
        fi
        echo ""
        echo "🏠 LOCAL ACCESS (from this pod):"
        echo "  Video Stream: http://localhost:8000/video_feed"
        echo "  Stream Health: http://localhost:8000/healthz"
        echo "  Remote API: http://localhost:5000/run"
        echo "  API Health: http://localhost:5000/healthz"
        ;;
        
    *)
        echo "WebCrawler Streamer Bot - Management Script"
        echo ""
        echo "Usage: ./manage.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start     - Start both services"
        echo "  stop      - Stop both services"
        echo "  restart   - Restart both services"
        echo "  status    - Show detailed status"
        echo "  logs      - Show recent logs (optional: stream|api)"
        echo "  tail      - Follow logs in real-time (stream|api)"
        echo "  test      - Run health checks and basic tests"
        echo "  urls      - Show all access URLs"
        echo ""
        echo "Examples:"
        echo "  ./manage.sh start              # Start services"
        echo "  ./manage.sh status             # Check status"
        echo "  ./manage.sh logs stream        # View Flask Stream logs"
        echo "  ./manage.sh tail api           # Follow API logs"
        echo "  ./manage.sh test               # Run tests"
        echo ""
        echo "Environment variables (optional):"
        echo "  START_URL            - Initial URL for stream (default: https://example.com)"
        echo "  FRAME_RATE_SECONDS   - Screenshot interval (default: 0.5)"
        echo ""
        echo "Example with custom URL:"
        echo "  START_URL='https://news.ycombinator.com' ./manage.sh restart"
        ;;
esac
