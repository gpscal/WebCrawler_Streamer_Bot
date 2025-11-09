Headless Selenium Web Streaming with Proxy on AWS

## 📘 Overview

This project demonstrates how to **run Selenium in headless mode on an AWS EC2 instance**, with live **video streaming** via Flask, **proxy rotation** for evading IP blocks, and **remote execution** capabilities.

---

## 🧠 Objectives

- Run **headless Selenium** (no GUI) for web automation/scraping.
- Stream browser activity in **real-time** over the network.
- Avoid IP bans using **rotating proxies**.
- Remotely trigger tasks from any device.
- Optimize for **RunPod RTX 4000/2000 Ada** GPU environments with turnkey deployment tooling.

---

## 🚀 RunPod GPU Deployment

### Hardware Profile

- 1 × **RTX 2000 Ada** (16 GB VRAM)
- 31 GB RAM, 6 vCPU
- 80 GB total disk

### 0. Prerequisites

- RunPod Ubuntu 22.04 (or compatible) template with NVIDIA drivers pre-installed.
- Public-facing ports open for `8000/tcp` (stream) and `5000/tcp` (remote control) or configure RunPod network rules accordingly.

### 1. Clone + Prepare

```bash
git clone https://github.com/<your-org>/WebCrawler_bot.git
cd WebCrawler_bot
chmod +x scripts/runpod_deploy.sh
```

### 2. Bootstrap & Launch

```bash
GPU_ENABLED=1 START_URL="https://example.com" FRAME_RATE_SECONDS=0.25 \
./scripts/runpod_deploy.sh
```

The script performs the following idempotent steps:

- Installs Google Chrome and matching ChromeDriver.
- Creates/updates the `selenium-env` virtual environment.
- Installs Python dependencies from `requirements.txt`.
- Launches `flask_stream.py` (video stream) and `remote_control.py` (task trigger) with GPU acceleration flags enabled.

You can override defaults via environment variables:

- `GPU_ENABLED=0` to force software rendering fallbacks.
- `START_URL`, `FRAME_RATE_SECONDS`, `JPEG_QUALITY`, `CAPTURE_MAX_WIDTH`, `CAPTURE_MAX_HEIGHT`.
- `HOST`, `PORT` for API binding.

### 3. Validate Runtime

```bash
curl http://<pod-ip>:8000/healthz
curl http://<pod-ip>:5000/healthz
curl http://<pod-ip>:5000/run?target_url=https://httpbin.org/ip
```

Open the live stream at `http://<pod-ip>:8000/video_feed`.

### 4. GPU Health Checks

```bash
nvidia-smi
curl http://<pod-ip>:8000/healthz | jq '.gpu_enabled'
```


---

## ⚙️ 1. AWS Setup

### 1.1 Launch EC2 Instance

- AMI: **Ubuntu 22.04 LTS** or **Amazon Linux 2**
- Instance Type: `t2.medium` (recommended)
- Open ports:
    - 22 → SSH access
    - 80 → HTTP (Flask app)
    - 443 → HTTPS (optional for secure streaming)
- Example IP: `3.133.87.114`

### 1.2 Secure Configuration

- Restrict inbound SSH to your public IP.
- Enable AWS CloudWatch for performance monitoring.
- Use **IAM roles** if you plan to store logs in S3 or interact with AWS APIs.

---

## 🧩 2. Install Dependencies

### 2.1 System Prep

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip unzip -y
```

### 2.2 Install Chrome and ChromeDriver

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
rm -rf chromedriver-linux64 chromedriver-linux64.zip
```

### 2.3 Install Python Libraries

```bash
python3 -m venv selenium-env
source selenium-env/bin/activate
pip install selenium flask pillow
```

---

## 🌐 3. Selenium Proxy Configuration

### 3.1 Base Headless Script – `selenium_worker.py`

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PROXY = "http://username:password@proxy-ip:port"  # Replace with your proxy

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(f"--proxy-server={PROXY}")

driver = webdriver.Chrome(options=options)
driver.get("https://httpbin.org/ip")  # Verify proxy usage
print(driver.page_source)
driver.quit()
```

### 3.2 Proxy Rotation Example

```python
proxies = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port"
]

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

for proxy in proxies:
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)
    driver.get("https://httpbin.org/ip")
    print(driver.page_source)
    driver.quit()
```

---

## 📡 4. Stream Browser Output with Flask

### 4.1 Flask Application – `flask_stream.py`

```python
from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import time

app = Flask(__name__)

def generate_frames(driver):
    while True:
        png = driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(png))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        frame = buf.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)  # control FPS

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(driver),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_opts)
    driver.get("https://example.com")
    app.run(host='0.0.0.0', port=8000, debug=False)
```

**Access Live Stream:**  
👉 `http://3.133.87.114:8000/video_feed`

---

## 🔒 5. Security & Remote Control

### 5.1 Basic API for Remote Control

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_script():
    # integrate Selenium run/crawl logic
    return jsonify({"status": "Task executed successfully"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

Access remotely:  
👉 `http://3.133.87.114:5000/run`

### 5.2 Optional SSH Tunnel (for secure local viewing)

```bash
ssh -L 8000:localhost:8000 ubuntu@3.133.87.114
```

Then open `http://localhost:8000/video_feed`.

---

## 🧪 6. Validation

|Test|Command|Expected Result|
|---|---|---|
|Proxy check|`python3 selenium_worker.py`|Shows proxy IP in output|
|Stream check|Open `http://<server-ip>:8000/video_feed`|Live browser stream|
|Remote trigger|`curl http://<server-ip>:5000/run`|JSON confirms script run|
|Network|`top`, `htop`, CloudWatch|CPU/network within limits|

---

## ⚡ 7. Optimization Tips

- Lower screenshot frequency (e.g., `time.sleep(1)` in `generate_frames()`).
- Use **rotating proxies** or **residential IPs** for heavy scraping.
- Schedule session resets to free browser memory.
- Optionally integrate CAPTCHA solvers (`2Captcha`, `AntiCaptcha`).

---

## 🛠️ 8. Deployment Checklist

|✅ Task|Description|
|---|---|
|🟩 EC2 Setup|Ubuntu or Amazon Linux, open ports 22/80/443|
|🟩 Dependencies Installed|Chrome, Chromedriver, Flask, Selenium|
|🟩 Proxy Configured|Static or Rotating proxy endpoint|
|🟩 Flask Stream Running|Accessible at `/video_feed`|
|🟩 Remote Script Trigger|`/run` endpoint online|
|🟩 Security Rules Set|Limited SSH, firewall rules applied|

---

### 📍 AWS Instance Reference

**Public IP:** `3.133.87.114`  
**Ports:** `22`, `80`, `443` open

---

### 🧰 Tech Stack

- **AWS EC2 (Ubuntu/AL2)**
- **Python 3**, **Selenium**
- **Chrome Headless + ChromeDriver**
- **Flask (streaming + control API)**
- **Pillow (image conversion)**
- **Proxy Integration (rotating or static)**
