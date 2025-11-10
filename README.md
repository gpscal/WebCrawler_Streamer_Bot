# 🚀 WebCrawler Streamer Bot

A powerful headless Selenium-based web crawler with real-time video streaming capabilities, running on RunPod GPU infrastructure.

## ✅ Current Status: DEPLOYED & RUNNING

---

## 🎯 Features

- **Real-time Browser Streaming**: Watch live browser activity via HTTP stream
- **Remote Web Crawling**: Trigger crawling tasks via REST API
- **GPU Acceleration**: Powered by NVIDIA RTX 4000 Ada (20GB VRAM)
- **Headless Chrome**: Fully automated browser automation
- **Proxy Support**: Optional proxy configuration for IP rotation
- **Health Monitoring**: Built-in health check endpoints

---

## 🌐 Quick Access

### Public URLs (Access from anywhere)

**Live Video Stream:**
```
http://157.157.221.29:24277/video_feed
```

**Remote Control API:**
```
http://157.157.221.29:24278/run
```

### Example Commands

**Crawl a Website:**
```bash
curl "http://157.157.221.29:24278/run?target_url=https://example.com"
```

**Check Your IP:**
```bash
curl "http://157.157.221.29:24278/run?target_url=https://httpbin.org/ip"
```

**With POST (JSON):**
```bash
curl -X POST http://157.157.221.29:24278/run \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://news.ycombinator.com"}'
```

**Using a Proxy:**
```bash
curl -X POST http://157.157.221.29:24278/run \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "proxy_url": "http://username:password@proxy-server:port"
  }'
```

---

## 🛠️ Management

Use the included management script for easy control:

```bash
# Show all available commands
./manage.sh

# Check status
./manage.sh status

# View logs
./manage.sh logs

# Follow logs in real-time
./manage.sh tail stream
./manage.sh tail api

# Run health tests
./manage.sh test

# Show all URLs
./manage.sh urls

# Restart services
./manage.sh restart

# Stop services
./manage.sh stop

# Start services
./manage.sh start
```

---

## 📊 System Information

- **Pod ID:** bw5lnjzg19928m
- **Location:** EUR-IS-1 (Iceland)
- **Public IP:** 157.157.221.29
- **GPU:** NVIDIA RTX 4000 Ada Generation (20GB VRAM)
- **Python:** 3.12.3
- **Chrome:** 142.0.7444.134
- **ChromeDriver:** 142.0.7444.134

### Port Mappings
- Port 8000 (Flask Stream) → Public Port 24277
- Port 5000 (Remote API) → Public Port 24278
- Port 22 (SSH) → Public Port 24276

---

## 📁 Project Structure

```
/WebCrawler_Streamer_Bot/
├── flask_stream.py         # Video streaming service
├── remote_control.py       # Remote control API
├── selenium_worker.py      # Selenium worker module
├── requirements.txt        # Python dependencies
├── manage.sh              # Management script ⭐
├── check_status.sh        # Status check script
├── QUICK_START.md         # Quick start guide
├── DEPLOYMENT_STATUS.md   # Detailed deployment info
├── implementation_plan.md # Architecture documentation
├── scripts/
│   └── runpod_deploy.sh   # Automated deployment
└── selenium-env/          # Python virtual environment
```

---

## 🔧 Configuration

### Environment Variables

**Flask Stream Service:**
- `GPU_ENABLED`: Enable GPU acceleration (default: 1)
- `START_URL`: Initial URL to load (default: https://example.com)
- `FRAME_RATE_SECONDS`: Screenshot interval (default: 0.5)
- `JPEG_QUALITY`: Image quality 1-100 (default: 85)
- `CAPTURE_MAX_WIDTH`: Max width (default: 1920)
- `CAPTURE_MAX_HEIGHT`: Max height (default: 1080)
- `PROXY_URL`: Optional proxy
- `HOST`: Bind address (default: 0.0.0.0)
- `PORT`: Port number (default: 8000)

**Remote Control Service:**
- `HOST`: Bind address (default: 0.0.0.0)
- `PORT`: Port number (default: 5000)
- `PROXY_URL`: Default proxy for crawling

### Custom Start Example
```bash
START_URL='https://news.ycombinator.com' \
FRAME_RATE_SECONDS=1.0 \
./manage.sh restart
```

---

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started quickly
- **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** - Full deployment details
- **[implementation_plan.md](implementation_plan.md)** - Architecture & design

---

## 🔍 Monitoring

### Check Service Status
```bash
./manage.sh status
```

### View Logs
```bash
# Recent logs (both services)
./manage.sh logs

# Stream service logs only
./manage.sh logs stream

# API service logs only
./manage.sh logs api

# Follow logs in real-time
./manage.sh tail stream
```

### Health Checks
```bash
# Check all services
./manage.sh test

# Or manually
curl http://157.157.221.29:24277/healthz
curl http://157.157.221.29:24278/healthz
```

---

## 🐛 Troubleshooting

### Services not responding?
```bash
./manage.sh status
./manage.sh logs
```

### Need to restart?
```bash
./manage.sh restart
```

### Chrome/Selenium issues?
```bash
# Check versions
google-chrome --version
chromedriver --version

# Test Selenium directly
cd /WebCrawler_Streamer_Bot
TARGET_URL="https://httpbin.org/ip" ./selenium-env/bin/python selenium_worker.py
```

### GPU not working?
```bash
nvidia-smi
```

---

## 🎓 API Reference

### Remote Control API

#### GET /run
Trigger a web crawling task.

**Parameters:**
- `target_url` (required): URL to crawl
- `proxy_url` (optional): Proxy server URL

**Example:**
```bash
curl "http://157.157.221.29:24278/run?target_url=https://example.com"
```

#### POST /run
Trigger a web crawling task with JSON payload.

**Body:**
```json
{
  "target_url": "https://example.com",
  "proxy_url": "http://user:pass@proxy:port"  // optional
}
```

**Response:**
```json
{
  "status": "Task executed successfully",
  "target_url": "https://example.com",
  "proxy_url": null,
  "timestamp": "2025-11-10T02:38:39.365156+00:00",
  "payload_preview": "<!DOCTYPE html>..."
}
```

#### GET /healthz
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### Flask Stream Service

#### GET /video_feed
Real-time video stream of browser activity.

**Response:** multipart/x-mixed-replace (MJPEG stream)

Open in browser to view live stream.

#### GET /healthz
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "start_url": "https://example.com",
  "frame_rate_seconds": 0.5,
  "jpeg_quality": 85,
  "gpu_enabled": "1"
}
```

---

## 🚀 Advanced Usage

### Proxy Rotation
```python
# You can rotate proxies by calling the API with different proxy_url values
proxies = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port"
]

for proxy in proxies:
    response = requests.post(
        "http://157.157.221.29:24278/run",
        json={"target_url": "https://example.com", "proxy_url": proxy}
    )
    print(response.json())
```

### Automated Crawling Script
```python
import requests
import time

def crawl_site(url):
    response = requests.get(
        f"http://157.157.221.29:24278/run",
        params={"target_url": url}
    )
    return response.json()

# Crawl multiple sites
sites = [
    "https://news.ycombinator.com",
    "https://example.com",
    "https://httpbin.org/ip"
]

for site in sites:
    result = crawl_site(site)
    print(f"Crawled: {site}")
    print(f"Preview: {result['payload_preview'][:100]}...")
    time.sleep(2)
```

---

## 📄 License

See LICENSE file for details.

---

## 🙏 Support

For issues or questions:
1. Check the logs: `./manage.sh logs`
2. Review documentation: `DEPLOYMENT_STATUS.md`
3. Run diagnostics: `./manage.sh test`

---

**Deployed on:** 2025-11-10  
**Status:** ✅ Fully Operational  
**Version:** 1.0.0
