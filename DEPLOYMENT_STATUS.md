# WebCrawler Streamer Bot - Deployment Status

## ✅ Deployment Complete!

**Date:** 2025-11-10  
**Instance:** RunPod GPU Instance (NVIDIA RTX 4000 Ada)

---

## 🎯 Services Running

### 1. Flask Stream Service (Port 8000)
- **Status:** ✅ Running
- **PID:** 4347
- **Log File:** `/WebCrawler_Streamer_Bot/flask_stream.log`
- **Configuration:**
  - GPU Enabled: Yes (RTX 4000 Ada)
  - Start URL: https://example.com
  - Frame Rate: 0.5 seconds (2 FPS)
  - JPEG Quality: 85
  - Max Resolution: 1920x1080

### 2. Remote Control API (Port 5000)
- **Status:** ✅ Running
- **PID:** 4560
- **Log File:** `/WebCrawler_Streamer_Bot/remote_control.log`

---

## 🌐 Access Information

### Pod Details
- **Pod ID:** bw5lnjzg19928m
- **Pod Hostname:** bw5lnjzg19928m-64411bc2
- **Data Center:** EUR-IS-1 (Iceland)
- **Internal IP:** 172.19.0.2
- **Public IP:** 157.157.221.29

### Port Mappings
- **SSH (22)** → Public Port: **24276**
- **Flask Stream (8000)** → Public Port: **24277**
- **Remote Control (5000)** → Public Port: **24278**

### 🔗 Public Access URLs

#### Local Access (from within the instance):
- **Video Stream:** http://localhost:8000/video_feed
- **Stream Health Check:** http://localhost:8000/healthz
- **Remote Control API:** http://localhost:5000/run
- **API Health Check:** http://localhost:5000/healthz

#### 🌍 External/Public Access:
- **Video Stream:** http://157.157.221.29:24277/video_feed
- **Stream Health Check:** http://157.157.221.29:24277/healthz
- **Remote Control API:** http://157.157.221.29:24278/run
- **API Health Check:** http://157.157.221.29:24278/healthz

**SSH Access:**
```bash
ssh -p 24276 root@157.157.221.29
```

---

## 🧪 Testing Commands

### Check Service Status
```bash
ps aux | grep -E "(flask_stream|remote_control)" | grep -v grep
```

### View Logs
```bash
# Flask Stream logs
tail -f /WebCrawler_Streamer_Bot/flask_stream.log

# Remote Control logs
tail -f /WebCrawler_Streamer_Bot/remote_control.log
```

### Test Health Endpoints
```bash
# Flask Stream
curl http://localhost:8000/healthz

# Remote Control
curl http://localhost:5000/healthz
```

### Test Web Crawling
```bash
curl "http://localhost:5000/run?target_url=https://httpbin.org/ip"
```

### Test with POST
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://example.com"}'
```

---

## 🔧 System Configuration

### Software Versions
- **OS:** Ubuntu 24.04 (Noble)
- **Python:** 3.12.3
- **Chrome:** 142.0.7444.134
- **ChromeDriver:** 142.0.7444.134
- **GPU:** NVIDIA RTX 4000 Ada (20GB VRAM)
- **CUDA:** 13.0
- **Driver:** 580.65.06

### Python Dependencies
- flask==3.1.2
- selenium==4.38.0
- pillow==10.4.0
- gunicorn==21.2.0

---

## 🚀 Restart Services

If you need to restart the services:

```bash
# Stop services
pkill -f flask_stream.py
pkill -f remote_control.py

# Start services again
cd /WebCrawler_Streamer_Bot

# Start Flask Stream
GPU_ENABLED=1 START_URL="https://example.com" FRAME_RATE_SECONDS=0.5 \
HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream.py > flask_stream.log 2>&1 &

# Start Remote Control
HOST=0.0.0.0 PORT=5000 \
nohup ./selenium-env/bin/python remote_control.py > remote_control.log 2>&1 &
```

---

## 📝 Environment Variables

### Flask Stream Service
- `GPU_ENABLED`: 1 (enabled) or 0 (disabled)
- `START_URL`: Initial URL to load
- `FRAME_RATE_SECONDS`: Screenshot interval
- `JPEG_QUALITY`: JPEG compression quality (1-100)
- `CAPTURE_MAX_WIDTH`: Max screenshot width (default: 1920)
- `CAPTURE_MAX_HEIGHT`: Max screenshot height (default: 1080)
- `PROXY_URL`: Optional proxy (format: http://user:pass@ip:port)
- `HOST`: Bind address (default: 0.0.0.0)
- `PORT`: Port number (default: 8000)

### Remote Control Service
- `HOST`: Bind address (default: 0.0.0.0)
- `PORT`: Port number (default: 5000)
- `PROXY_URL`: Optional proxy for crawling tasks

---

## 🎨 Usage Examples

### View Live Browser Stream
Open in your browser (after configuring RunPod port forwarding):
```
http://<runpod-public-url>:8000/video_feed
```

### Trigger Web Crawling Tasks

#### Simple GET request:
```bash
curl "http://<your-ip>:5000/run?target_url=https://example.com"
```

#### With proxy:
```bash
curl "http://<your-ip>:5000/run?target_url=https://example.com&proxy_url=http://user:pass@proxy:port"
```

#### POST with JSON:
```bash
curl -X POST http://<your-ip>:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "proxy_url": "http://user:pass@proxy:port"
  }'
```

---

## 🔒 Security Notes

⚠️ **Important:** These services are currently running in development mode.

For production deployment, consider:
1. Using gunicorn instead of Flask's development server
2. Adding authentication to the API endpoints
3. Enabling HTTPS/TLS
4. Restricting IP access via firewall rules
5. Setting up proper logging and monitoring

---

## 📞 Next Steps

1. **Configure RunPod Port Forwarding:**
   - Go to your RunPod dashboard
   - Find your pod settings
   - Expose ports 8000 and 5000
   - Note the public URLs provided

2. **Test External Access:**
   - Use the RunPod-provided URL to access the video stream
   - Test the remote control API from your local machine

3. **Optional: Set up systemd services** for auto-restart on reboot
4. **Optional: Configure proxy rotation** for production scraping

---

## 🐛 Troubleshooting

### Service won't start
```bash
# Check logs
tail -50 /WebCrawler_Streamer_Bot/flask_stream.log
tail -50 /WebCrawler_Streamer_Bot/remote_control.log

# Check if ports are in use
ss -tlnp | grep -E "(8000|5000)"
```

### Chrome/ChromeDriver issues
```bash
# Verify versions match
google-chrome --version
chromedriver --version

# Test Selenium directly
cd /WebCrawler_Streamer_Bot
TARGET_URL="https://httpbin.org/ip" ./selenium-env/bin/python selenium_worker.py
```

### GPU not working
```bash
# Check GPU status
nvidia-smi

# Verify GPU environment variable
echo $GPU_ENABLED
```

---

**Status:** All services operational ✅  
**Last Updated:** 2025-11-10 02:33 UTC
