# 🤖 Human-Like Behavior Guide

## Overview

The enhanced WebCrawler Streamer Bot now includes realistic human-like behavior:
- **Smooth scrolling** with natural pauses
- **Automatic "Next Page" detection** and clicking
- **Random delays** and micro-movements
- **Continuous streaming** while navigating

---

## 🚀 Quick Start

### Option 1: Automatic Mode (Recommended)

The bot will automatically scroll and click "Next Page" buttons while streaming:

```bash
# Stop old service
pkill -f flask_stream.py

# Start enhanced service with auto-scroll and auto-next
cd /WebCrawler_Streamer_Bot
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://news.ycombinator.com" \
GPU_ENABLED=1 FRAME_RATE_SECONDS=0.5 HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &
```

**Watch it live:**
```
http://157.157.221.29:24277/video_feed
```

The bot will:
1. Load your website
2. Wait 10 seconds
3. Scroll down slowly (like reading)
4. Look for "Next Page" button
5. Click it if found
6. Repeat on new page

---

## 📡 API Endpoints

### GET /video_feed
Live video stream (same as before)

### GET /healthz
Enhanced health check with state information

**Response:**
```json
{
  "status": "ok",
  "current_url": "https://example.com/page/2",
  "auto_scroll_enabled": true,
  "auto_next_enabled": true,
  "last_action": "loaded_page_2",
  "page_count": 2,
  "is_scrolling": false
}
```

### POST /navigate
Navigate to a new URL with human-like behavior

**Request:**
```bash
curl -X POST http://157.157.221.29:24277/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "scroll": true,
    "find_next": true
  }'
```

**Response:**
```json
{
  "url": "https://news.ycombinator.com",
  "success": true,
  "scrolled": true,
  "next_page_found": true,
  "next_page_clicked": true,
  "next_url": "https://news.ycombinator.com/news?p=2"
}
```

### POST /scroll
Manually trigger scrolling

**Request:**
```bash
curl -X POST http://157.157.221.29:24277/scroll \
  -H "Content-Type: application/json" \
  -d '{"num_scrolls": 5}'
```

### POST /next_page
Find and click next page button

**Request:**
```bash
curl -X POST http://157.157.221.29:24277/next_page
```

**Response:**
```json
{
  "success": true,
  "new_url": "https://example.com/page/2",
  "page_count": 2
}
```

### GET/POST /config
Get or update configuration

**Get config:**
```bash
curl http://157.157.221.29:24277/config
```

**Update config:**
```bash
curl -X POST http://157.157.221.29:24277/config \
  -H "Content-Type: application/json" \
  -d '{
    "auto_scroll_enabled": true,
    "auto_next_enabled": false
  }'
```

---

## 🎮 Usage Examples

### Example 1: Automatic News Browsing

```bash
# Start with Hacker News
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://news.ycombinator.com" \
SCROLL_INTERVAL=15 ./selenium-env/bin/python flask_stream_enhanced.py
```

Watch as the bot:
- Scrolls down the page
- Finds the "More" link
- Clicks it
- Loads page 2
- Continues browsing

### Example 2: E-commerce Product Browsing

```bash
# Browse product listings
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://example-shop.com/products" \
SCROLL_INTERVAL=20 ./selenium-env/bin/python flask_stream_enhanced.py
```

### Example 3: Manual Control

```bash
# Start without auto-scroll
AUTO_SCROLL=0 START_URL="https://example.com" \
./selenium-env/bin/python flask_stream_enhanced.py
```

Then control via API:
```bash
# Scroll when you want
curl -X POST http://localhost:8000/scroll -H "Content-Type: application/json" -d '{"num_scrolls": 3}'

# Navigate to new page
curl -X POST http://localhost:8000/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://another-site.com", "scroll": true, "find_next": true}'

# Click next page
curl -X POST http://localhost:8000/next_page
```

---

## ⚙️ Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTO_SCROLL` | `1` | Enable automatic scrolling |
| `AUTO_NEXT` | `1` | Enable automatic next page clicking |
| `SCROLL_INTERVAL` | `10.0` | Seconds between auto-scrolls |
| `START_URL` | `https://example.com` | Initial URL |
| `FRAME_RATE_SECONDS` | `0.5` | Video stream frame rate |
| `GPU_ENABLED` | `1` | GPU acceleration |
| `PROXY_URL` | None | Optional proxy |

### Human Behavior Settings

The bot uses these realistic patterns:

**Scrolling:**
- Scrolls 30% of viewport height at a time
- Random pauses: 1-2.5 seconds
- Occasional scroll-back (10% chance) - like re-reading
- Smooth easing curves for natural motion

**Next Page Detection:**
- Searches for: "next", "next page", ">", "»", "→"
- Checks: links, buttons, aria-labels, pagination containers
- Multi-language support: English, Spanish, French, German, Portuguese, Japanese, Chinese

**Clicking:**
- Scrolls element into view first
- Random delay before click (0.3-0.8s)
- Moves mouse to element with curve
- Hovers briefly (0.2-0.5s)
- Then clicks

---

## 🎯 Real-World Use Cases

### 1. News Aggregator Monitoring
```bash
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://news.ycombinator.com" \
SCROLL_INTERVAL=30 ./selenium-env/bin/python flask_stream_enhanced.py
```
Browse through pages of news automatically.

### 2. Product Catalog Scraping
```bash
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://shop.example.com/category" \
SCROLL_INTERVAL=25 ./selenium-env/bin/python flask_stream_enhanced.py
```
Navigate through product listings page by page.

### 3. Social Media Feed Browsing
```bash
AUTO_SCROLL=1 AUTO_NEXT=0 START_URL="https://social-site.com/feed" \
SCROLL_INTERVAL=15 ./selenium-env/bin/python flask_stream_enhanced.py
```
Continuous scrolling without next page (infinite scroll sites).

### 4. Search Results Navigation
```bash
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://search.example.com/q=test" \
SCROLL_INTERVAL=20 ./selenium-env/bin/python flask_stream_enhanced.py
```
Automatically browse through search result pages.

---

## 🔧 Troubleshooting

### Next Page Not Found?

The bot looks for these patterns:
- Text: "next", "next page", ">", "»", "→"
- Classes: `.next`, `.pagination-next`, `.page-next`
- Attributes: `[rel='next']`, `[aria-label*='next']`
- Multi-language variants

If your site uses different patterns, you can modify `human_behavior.py`:

```python
# Add custom patterns in HumanBehavior class
NEXT_PAGE_PATTERNS = [
    "custom-next-class",
    "your-specific-text",
]
```

### Bot Scrolling Too Fast/Slow?

Adjust the intervals:
```bash
SCROLL_INTERVAL=30  # Wait 30 seconds between scrolls
```

Or modify scroll behavior in API:
```bash
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"auto_scroll_enabled": false}'
```

### Check Current State

```bash
curl http://157.157.221.29:24277/healthz | jq
```

Shows:
- Current URL
- Page count
- Last action
- Auto-scroll status
- Auto-next status

---

## 📊 Monitoring

### Watch the logs
```bash
tail -f /WebCrawler_Streamer_Bot/flask_stream_enhanced.log
```

### Check status periodically
```bash
watch -n 5 'curl -s http://localhost:8000/healthz | jq'
```

### View live stream
Open in browser:
```
http://157.157.221.29:24277/video_feed
```

---

## 🎬 Demo Workflow

1. **Start the enhanced service:**
```bash
./manage.sh stop
cd /WebCrawler_Streamer_Bot
AUTO_SCROLL=1 AUTO_NEXT=1 START_URL="https://news.ycombinator.com" \
GPU_ENABLED=1 HOST=0.0.0.0 PORT=8000 \
nohup ./selenium-env/bin/python flask_stream_enhanced.py > flask_stream_enhanced.log 2>&1 &
```

2. **Open the video stream:**
```
http://157.157.221.29:24277/video_feed
```

3. **Watch it work:**
   - Loads Hacker News
   - Scrolls down slowly
   - Finds "More" link at bottom
   - Clicks it
   - Loads page 2
   - Continues automatically

4. **Check status:**
```bash
curl http://157.157.221.29:24277/healthz | jq
```

5. **Navigate manually if needed:**
```bash
curl -X POST http://157.157.221.29:24277/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/trending", "scroll": true, "find_next": true}'
```

---

## 🔥 Pro Tips

1. **Watch while developing:** Keep the video stream open to see exactly what's happening

2. **Adjust timing for the site:** Some sites need more time to load:
   ```bash
   SCROLL_INTERVAL=30  # Slower for heavy sites
   ```

3. **Disable auto-next for infinite scroll:**
   ```bash
   AUTO_SCROLL=1 AUTO_NEXT=0  # Just scroll, no next button
   ```

4. **Use with proxy for heavy scraping:**
   ```bash
   PROXY_URL="http://user:pass@proxy:port" ./selenium-env/bin/python flask_stream_enhanced.py
   ```

5. **Combine with remote control API:** Stream one site, control another via API

---

## 📖 Next Steps

See the full API documentation and examples in the README.md file.

For deployment and management, use the `manage.sh` script with enhanced options.
