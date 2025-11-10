#!/bin/bash
# Demo script for enhanced human-like behavior

echo "================================================"
echo "WebCrawler Streamer Bot - Enhanced Demo"
echo "================================================"
echo ""

# Check if service is running
if ! pgrep -f "flask_stream_enhanced.py" > /dev/null; then
    echo "❌ Enhanced service is not running!"
    echo ""
    echo "Start it with:"
    echo "  cd /WebCrawler_Streamer_Bot"
    echo "  AUTO_SCROLL=1 AUTO_NEXT=1 START_URL='https://news.ycombinator.com' \\"
    echo "  GPU_ENABLED=1 HOST=0.0.0.0 PORT=8000 \\"
    echo "  nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &"
    exit 1
fi

echo "✅ Enhanced service is running!"
echo ""

# Get current status
echo "📊 Current Status:"
echo "=================="
curl -s http://localhost:8000/healthz | python3 -m json.tool
echo ""

# Public URLs
echo "🌐 Access URLs:"
echo "==============="
if [ -n "$RUNPOD_PUBLIC_IP" ] && [ -n "$RUNPOD_TCP_PORT_8000" ]; then
    echo "Video Stream: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_8000}/video_feed"
    echo "Health Check: http://${RUNPOD_PUBLIC_IP}:${RUNPOD_TCP_PORT_8000}/healthz"
else
    echo "Video Stream: http://localhost:8000/video_feed"
    echo "Health Check: http://localhost:8000/healthz"
fi
echo ""

echo "🎮 Available Actions:"
echo "===================="
echo ""
echo "1. Watch Live Stream"
echo "   Open in browser: http://157.157.221.29:24277/video_feed"
echo ""
echo "2. Check Status"
echo "   curl http://localhost:8000/healthz | jq"
echo ""
echo "3. Navigate to New URL"
echo "   curl -X POST http://localhost:8000/navigate \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"url\": \"https://github.com/trending\", \"scroll\": true, \"find_next\": true}'"
echo ""
echo "4. Manually Scroll"
echo "   curl -X POST http://localhost:8000/scroll \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"num_scrolls\": 5}'"
echo ""
echo "5. Click Next Page"
echo "   curl -X POST http://localhost:8000/next_page"
echo ""
echo "6. Toggle Auto-Scroll"
echo "   curl -X POST http://localhost:8000/config \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"auto_scroll_enabled\": false}'"
echo ""
echo "7. View Logs"
echo "   tail -f /WebCrawler_Streamer_Bot/flask_stream_enhanced.log"
echo ""

# Offer to run a demo
echo "================================================"
echo ""
read -p "Run a quick demo? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎬 Running Demo..."
    echo ""
    
    echo "Step 1: Current status"
    curl -s http://localhost:8000/healthz | python3 -m json.tool
    echo ""
    sleep 2
    
    echo "Step 2: Manually trigger scroll..."
    curl -X POST http://localhost:8000/scroll \
      -H 'Content-Type: application/json' \
      -d '{"num_scrolls": 3}'
    echo ""
    sleep 5
    
    echo "Step 3: Try to click next page..."
    curl -X POST http://localhost:8000/next_page | python3 -m json.tool
    echo ""
    sleep 2
    
    echo "Step 4: Final status"
    curl -s http://localhost:8000/healthz | python3 -m json.tool
    echo ""
    
    echo "✅ Demo complete!"
    echo ""
    echo "Watch the live stream to see it in action:"
    echo "http://157.157.221.29:24277/video_feed"
fi

echo ""
echo "================================================"
echo "For more info, see: HUMAN_BEHAVIOR_GUIDE.md"
echo "================================================"
