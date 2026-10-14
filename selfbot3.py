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
        self.wfile.write(b"Trade-Ideas Bot is Running 24/7!")

    def log_message(self, format, *args):
        return  # Clean logs

def start_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        server.serve_forever()
    except Exception as e:
        print(f"[SERVER WARN] Port binding bypassed: {e}", flush=True)

# Background HTTP server start
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# ----------------- 2. DISCORD AUTO-POSTER LOGIC ----------------- #
USER_TOKEN = os.environ.get("USER_TOKEN", "YOUR_DISCORD_TOKEN_HERE")

# trade-ideas channel ki ID yahan paste karein
CHANNEL_ID = "1297596458337439754"

paragraphs = [
    "Trading rules exist to protect you from your own worse impulses.\nDo not modify your stop-loss mid-trade to give a loser 'breathing room'.\nRespect the boundary you set when your head was clear.",
    "A setup without confirmation is just a prediction.\nWait for the market to prove your thesis right before committing capital.\nPatience is the most profitable indicator.",
    "Risk management precedes profitability.\nNever risk more than your predefined allocation on a single trade setup.\nPreserving capital guarantees you stay in the game.",
    "Market structure ALWAYS overrides individual indicator signals.\nIf market structure is bearish, ignore bullish momentum divergence on lower timeframes.\nTrade with the higher timeframe flow.",
    "The best trade setups usually feel uncomfortable to execute.\nWhen price reaches a key liquidity pool or demand zone, execution requires discipline over emotion.",
    "Stop chasing breakouts after the move has already extended.\nWait for liquidity sweeps and retests of key structural levels to get a proper risk-to-reward entry.",
    "Consistency comes from executing a proven edge repeatedly.\nDo not switch strategies after a few losing trades; drawdown is a natural part of trading."
]

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json"
}

available_paragraphs = paragraphs.copy()
random.shuffle(available_paragraphs)
msg_count = 0

print("[+] Trade-Ideas Auto-Poster Started!", flush=True)

while True:
    try:
        if not available_paragraphs:
            available_paragraphs = paragraphs.copy()
            random.shuffle(available_paragraphs)
            print("[INFO] Reshuffled trade ideas paragraphs.", flush=True)

        message = available_paragraphs.pop()
        data = {"content": message}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in (200, 201):
            msg_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Trade-Ideas Msg #{msg_count} Sent Successfully!", flush=True)
            
            # Exactly 2 minutes delay (120 to 130 seconds)
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
