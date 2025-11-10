# 🚀 WebCrawler Streamer Bot - Quick Start Guide

## ✅ Deployment Status: COMPLETE

Your WebCrawler Streamer Bot has been successfully deployed on your RunPod instance!

---

## 🌐 Your Pod Information

- **Pod ID:** `bw5lnjzg19928m`
- **Location:** EUR-IS-1 (Iceland)
- **GPU:** NVIDIA RTX 4000 Ada (20GB VRAM)
- **Public IP:** `157.157.221.29`

---

## 🔗 Access Your Services

### Video Stream (Live Browser View)
Open this URL in your web browser to see the live stream:

```
http://157.157.221.29:24277/video_feed
```

### Remote Control API
Trigger web crawling tasks using these URLs:

**Health Check:**
```bash
curl http://157.157.221.29:24278/healthz
```

**Crawl a Website:**
```bash
curl "http://157.157.221.29:24278/run?target_url=https://example.com"
```

**With POST (JSON):**
```bash
curl -X POST http://157.157.221.29:24278/run \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://www.google.com"}'
```

---

## 📊 Service Status

Both services are running and ready:

| Service | Port | Status | PID |
|---------|------|--------|-----|
| Flask Stream | 8000 → 24277 | ✅ Running | 4347 |
| Remote Control | 5000 → 24278 | ✅ Running | 4560 |

---

## 🛠️ Management Commands

### Check Service Status
```bash
ps aux | grep -E "(flask_stream|remote_control)" | grep -v grep
```

### View Real-Time Logs
```bash
# Flask Stream logs
tail -f /WebCrawler_Streamer_Bot/flask_stream.log

# Remote Control logs  
tail -f /WebCrawler_Streamer_Bot/remote_control.log
```

### Restart Services
```bash
# Stop services
pkill -f flask_stream.py
pkill -f remote_control.py

# Start services
cd /WebCrawler_Streamer_Bot

GPU_ENABLED=1 START_URL="https://example.com" FRAME_RATE_SECONDS=0.5 \
HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream.py > flask_stream.log 2>&1 &

HOST=0.0.0.0 PORT=5000 \
nohup ./selenium-env/bin/python remote_control.py > remote_control.log 2>&1 &
```

---

## 🎮 Try It Out!

### Example 1: Check Your IP
```bash
curl "http://157.157.221.29:24278/run?target_url=https://httpbin.org/ip"
```

### Example 2: Crawl a Website
```bash
curl "http://157.157.221.29:24278/run?target_url=https://news.ycombinator.com"
```

### Example 3: Use with Proxy
```bash
curl -X POST http://157.157.221.29:24278/run \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "proxy_url": "http://username:password@proxy-server:port"
  }'
```

---

## 📝 Configuration Options

You can customize the services by setting environment variables before starting:

### Flask Stream Options:
- `START_URL`: Initial URL to display (default: https://example.com)
- `FRAME_RATE_SECONDS`: Screenshot interval (default: 0.5)
- `JPEG_QUALITY`: Image quality 1-100 (default: 85)
- `GPU_ENABLED`: Use GPU acceleration (default: 1)
- `PROXY_URL`: Optional proxy for the stream

### Remote Control Options:
- `PROXY_URL`: Default proxy for crawling tasks

---

## 🔍 Troubleshooting

### Can't access the services from outside?

**From outside the pod:**
- Make sure you're using the public IP: `157.157.221.29`
- Make sure you're using the mapped ports: `24277` and `24278`

**From inside the pod (SSH):**
- Use `localhost` and original ports: `8000` and `5000`

### Services not running?

Check the logs:
```bash
tail -50 /WebCrawler_Streamer_Bot/flask_stream.log
tail -50 /WebCrawler_Streamer_Bot/remote_control.log
```

### Need to test from inside the pod?
```bash
# Health checks
curl http://localhost:8000/healthz
curl http://localhost:5000/healthz

# Test crawling
curl "http://localhost:5000/run?target_url=https://httpbin.org/ip"
```

---

## 📚 Documentation Files

- **Full Details:** See `DEPLOYMENT_STATUS.md` for complete deployment information
- **Implementation Plan:** See `implementation_plan.md` for architecture details
- **Scripts:** Check `scripts/runpod_deploy.sh` for automated deployment

---

## 🎉 You're All Set!

Your WebCrawler Streamer Bot is now running and accessible. Open the video stream URL in your browser to watch it in action!

**Video Stream:** http://157.157.221.29:24277/video_feed

**Remote Control API:** http://157.157.221.29:24278/run

---

**Need Help?** Check the logs or the full deployment documentation in `DEPLOYMENT_STATUS.md`.
