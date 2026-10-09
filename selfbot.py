import time
import random
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Render deployment ke liye dynamic PORT handle karne wala HTTP server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running 24/7!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# ----------------- Discord Bot Code ----------------- #

USER_TOKEN = "MTU1MDgwMDQwNDI2MDk3ODc0OQ.GJNn7p.fAsB0TqLqKLkaAnLmqM_fczFZOVxdKYcbp1eM4"
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

print("[+] Secondary Account Auto-Poster Started!")

while True:
    try:
        if not available_paragraphs:
            available_paragraphs = paragraphs.copy()
            random.shuffle(available_paragraphs)
            print("[INFO] Reshuffled paragraphs.")

        message = available_paragraphs.pop()
        data = {"content": message}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in (200, 201):
            msg_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Message #{msg_count} Sent Successfully!")
            wait_time = random.randint(305, 320)
            print(f"[WAIT] Next message in {wait_time // 60} minutes ({wait_time} seconds)...")
            time.sleep(wait_time)

        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 120)
            print(f"[RATE LIMIT] Waiting for {retry_after} seconds...")
            time.sleep(retry_after + 5)

        else:
            print(f"[ERROR] Failed. Code: {response.status_code}, Response: {response.text}")
            time.sleep(15)

    except Exception as e:
        print(f"[EXCEPTION] Error: {e}")
        time.sleep(15)
