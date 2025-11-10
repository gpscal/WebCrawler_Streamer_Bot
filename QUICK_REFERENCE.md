# 🚀 Quick Reference - Enhanced WebCrawler Bot

## ⚡ TL;DR

Your bot is **LIVE** and automatically browsing the web right now!

**Watch:** http://157.157.221.29:24277/video_feed  
**Status:** `curl http://157.157.221.29:24277/healthz | jq`

---

## 🎯 What It Does

The bot acts like a human:
1. ✅ Loads a webpage
2. ✅ Scrolls down slowly (like reading)
3. ✅ Finds "Next Page" button
4. ✅ Clicks it
5. ✅ Repeats on new page
6. ✅ Streams everything live

**Currently browsing:** Page 3 of Hacker News, now viewing a GitHub repo!

---

## 📺 Watch Live Stream

Open in your browser:
```
http://157.157.221.29:24277/video_feed
```

You'll see the bot browsing in real-time!

---

## 🎮 Quick Commands

### Check Status
```bash
curl http://157.157.221.29:24277/healthz | jq
```

### Navigate to a Website
```bash
curl -X POST http://157.157.221.29:24277/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/trending", "scroll": true, "find_next": true}'
```

### Scroll Manually (5 times)
```bash
curl -X POST http://157.157.221.29:24277/scroll \
  -H "Content-Type: application/json" \
  -d '{"num_scrolls": 5}'
```

### Click Next Page
```bash
curl -X POST http://157.157.221.29:24277/next_page
```

### Turn Off Auto-Scroll
```bash
curl -X POST http://157.157.221.29:24277/config \
  -H "Content-Type: application/json" \
  -d '{"auto_scroll_enabled": false, "auto_next_enabled": false}'
```

### Turn On Auto-Scroll
```bash
curl -X POST http://157.157.221.29:24277/config \
  -H "Content-Type: application/json" \
  -d '{"auto_scroll_enabled": true, "auto_next_enabled": true}'
```

---

## 🔧 Service Management

### Check if Running
```bash
ps aux | grep flask_stream_enhanced | grep -v grep
```

### View Logs
```bash
tail -f /WebCrawler_Streamer_Bot/flask_stream_enhanced.log
```

### Stop Service
```bash
pkill -f flask_stream_enhanced.py
```

### Start Service
```bash
cd /WebCrawler_Streamer_Bot
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://news.ycombinator.com" \
GPU_ENABLED=1 HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &
```

### Restart with Different URL
```bash
pkill -f flask_stream_enhanced.py
cd /WebCrawler_Streamer_Bot
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://your-site.com" \
GPU_ENABLED=1 HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &
```

---

## 📊 Understanding the Status

When you run `curl http://157.157.221.29:24277/healthz | jq`, you see:

```json
{
  "status": "ok",                          ← Service is healthy
  "current_url": "https://...",            ← What page it's on
  "page_count": 3,                         ← How many pages it's visited
  "auto_scroll_enabled": true,             ← Auto-scroll is ON
  "auto_next_enabled": true,               ← Auto next-page is ON
  "is_scrolling": false,                   ← Currently scrolling?
  "last_action": "loaded_page_3"          ← What it just did
}
```

### Possible `last_action` Values:
- `initialized` - Just started
- `idle` - Waiting
- `auto_scrolling` - Automatically scrolling
- `manual_scrolling` - You triggered scroll
- `manual_navigation` - You navigated to URL
- `clicking_next_page` - Found and clicking Next
- `loaded_page_N` - Loaded page N

---

## 🎯 Use Cases

### 1. News Site Monitoring
```bash
# Start on news site
pkill -f flask_stream_enhanced.py
START_URL="https://news.ycombinator.com" ./selenium-env/bin/python flask_stream_enhanced.py
```

### 2. E-Commerce Browsing
```bash
START_URL="https://shop.example.com/products" ./selenium-env/bin/python flask_stream_enhanced.py
```

### 3. Search Results
```bash
START_URL="https://search.example.com/q=test" ./selenium-env/bin/python flask_stream_enhanced.py
```

### 4. Manual Control
```bash
# Disable auto features
AUTO_SCROLL=0 AUTO_NEXT=0 START_URL="https://example.com" \
./selenium-env/bin/python flask_stream_enhanced.py
```

Then control via API commands.

---

## 🌐 All Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/video_feed` | GET | Live video stream |
| `/healthz` | GET | Status check |
| `/navigate` | POST | Go to URL with scrolling |
| `/scroll` | POST | Scroll manually |
| `/next_page` | POST | Click next button |
| `/config` | GET/POST | View/update settings |

---

## 💡 Pro Tips

1. **Keep stream open** - Watch what's happening in real-time
2. **Check status often** - See page count increase
3. **Adjust timing** - Use `SCROLL_INTERVAL=30` for slower browsing
4. **Save URLs** - Track where it's been via `current_url`
5. **Log errors** - Check logs if something goes wrong

---

## 📚 More Info

- **ENHANCED_FEATURES.md** - Feature overview
- **HUMAN_BEHAVIOR_GUIDE.md** - Complete API docs
- **README.md** - Project documentation
- **demo_enhanced.sh** - Run interactive demo

---

## 🎉 Quick Demo

Run this:
```bash
./demo_enhanced.sh
```

It will show you everything the bot can do!

---

## ❓ Troubleshooting

### Can't see video stream?
Open: http://157.157.221.29:24277/video_feed

### Bot not finding Next button?
It looks for: "next", "next page", ">", "»", "→", `.next`, `[rel='next']`, and more

### Want to slow it down?
```bash
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"auto_scroll_enabled": false}'
```

### Check what it's doing?
```bash
curl http://localhost:8000/healthz | jq ".last_action, .current_url, .page_count"
```

---

## 🔥 Currently Active

Right now, your bot is:
- ✅ Running on port 8000
- ✅ Auto-scrolling enabled
- ✅ Auto-next enabled
- ✅ GPU acceleration active
- ✅ Streaming at 2 FPS
- ✅ Has visited 3+ pages already!

**Start watching:** http://157.157.221.29:24277/video_feed

---

**Your WebCrawler Bot is ready! Enjoy! 🎉**
