import time
import random
import requests
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ----------------- 1. DUMMY HTTP SERVER FOR RENDER ----------------- #
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is Running 24/7!")

    def log_message(self, format, *args):
        return  # Render logs clean rakhne ke liye HTTP logs disable kiye hain

def start_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Background me Web Server start karein
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# ----------------- 2. DISCORD AUTO-POSTER LOGIC ----------------- #
USER_TOKEN = os.environ.get("USER_TOKEN")
CHANNEL_ID = "1410924658840178738"

paragraphs = [
    "Order flow analysis gives traders a deeper look into the actual buying and selling transactions taking place in real time.",
    "Volume spread analysis focuses on the relationship between price spread, volume, and closing price of individual bars.",
    "Fibonacci retracement levels are mathematical reference points derived from natural sequences.",
    "Moving averages are among the most popular trend-following tools because they smooth out price fluctuations.",
    "Momentum divergence occurs when price makes a new extreme while an oscillator fails to confirm it.",
    "Volatility squeezes occur during extended periods of market consolidation where price compression reaches extreme levels.",
    "Trailing stop-loss orders allow traders to protect accumulated profits while giving winning positions room to capture trends.",
    "Fixed fractional position sizing is a risk management method where a trader risks the exact same percentage.",
    "Mental capital is just as important as financial capital for active market participants."
]

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json"
}

available_paragraphs = paragraphs.copy()
random.shuffle(available_paragraphs)
msg_count = 0

print("[+] Secondary Account Auto-Poster Started!", flush=True)

# App start hote hi pehla message turant bhejne ke liye
while True:
    try:
        if not available_paragraphs:
            available_paragraphs = paragraphs.copy()
            random.shuffle(available_paragraphs)
            print("[INFO] Reshuffled paragraphs.", flush=True)

        message = available_paragraphs.pop()
        data = {"content": message}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in (200, 201):
            msg_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Message #{msg_count} Sent Successfully!", flush=True)
            wait_time = random.randint(305, 320)
            print(f"[WAIT] Next message in {wait_time // 60} minutes ({wait_time} seconds)...", flush=True)
            time.sleep(wait_time)

        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 120)
            print(f"[RATE LIMIT] Waiting for {retry_after} seconds...", flush=True)
            time.sleep(retry_after + 5)

        else:
            print(f"[ERROR] Failed. Code: {response.status_code}, Response: {response.text}", flush=True)
            time.sleep(15)

    except Exception as e:
        print(f"[EXCEPTION] Error: {e}", flush=True)
        time.sleep(15)
