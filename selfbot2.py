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
        self.wfile.write(b"Games Chat Bot is Running 24/7!")

    def log_message(self, format, *args):
        return  # Render logs clean rakhne ke liye HTTP logs disable kiye hain

def start_server():
    # Dusri script se port collision na ho isliye alternative port check
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        server.serve_forever()
    except Exception as e:
        print(f"[SERVER WARN] Could not start server on port {port}: {e}", flush=True)

# Background me Web Server start karein
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# ----------------- 2. DISCORD AUTO-POSTER LOGIC ----------------- #
# Render / Env variable se USER_TOKEN uthayega (ya yahan direct fallback token daal sakte hain)
USER_TOKEN = os.environ.get("USER_TOKEN", "YOUR_DISCORD_TOKEN_HERE")

# Games Chat Channel ID
CHANNEL_ID = "1216836991942135859"

paragraphs = [
    "The real edge in trading is behavioral — doing consistently what most people cannot do emotionally.",
    "High-probability trading is often repetitive and quietly boring.",
    "If you are trading for adrenaline, visit a casino instead.",
    "Seek execution precision, not cheap emotional thrills.",
    "Risk management is the key to longevity in trading.",
    "Stick to your plan, respect your stop loss, and let the trade play out.",
    "Trading is a marathon, not a sprint. Consistency over speed.",
    "Master your psychology before you try to master the markets.",
    "Patience in waiting for the right setup is just as important as the trade itself.",
    "Focus on process over outcome. A good trade can lose money, but execution is what counts.",
    "Small consistent wins compound into massive gains over time.",
    "Never let a winning trade turn into a losing trade out of greed."
]

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json"
}

available_paragraphs = paragraphs.copy()
random.shuffle(available_paragraphs)
msg_count = 0

print("[+] Games-Chat Auto-Poster Started!", flush=True)

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
            print(f"[{time.strftime('%H:%M:%S')}] Games-Chat Msg #{msg_count} Sent Successfully!", flush=True)
            
            # Exactly 2 Minutes (120 to 130 seconds random delay for safety)
            wait_time = random.randint(120, 130)
            print(f"[WAIT] Next message in {wait_time // 60} minutes ({wait_time} seconds)...", flush=True)
            time.sleep(wait_time)

        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 60)
            print(f"[RATE LIMIT] Waiting for {retry_after} seconds...", flush=True)
            time.sleep(retry_after + 5)

        else:
            print(f"[ERROR] Failed. Code: {response.status_code}, Response: {response.text}", flush=True)
            time.sleep(15)

    except Exception as e:
        print(f"[EXCEPTION] Error: {e}", flush=True)
        time.sleep(15)
