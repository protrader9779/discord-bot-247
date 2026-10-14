import requests
import time
import random

# Discord Token aur Channel ID Yahan Dalein
TOKEN = "YOUR_DISCORD_TOKEN_HERE"
CHANNEL_ID = "1216836991942135859"  # games-chat channel ID

# Trading related quotes aur messages ki list
MESSAGES = [
    "The real edge in trading is behavioral — doing consistently what most people cannot do emotionally.",
    "High-probability trading is often repetitive and quietly boring.",
    "If you are trading for adrenaline, visit a casino instead.",
    "Seek execution precision, not cheap emotional thrills.",
    "Risk management is the key to longevity in trading.",
    "Stick to your plan, respect your stop loss, and let the trade play out.",
    "Trading is a marathon, not a sprint. Consistency over speed.",
    "Master your psychology before you try to master the markets."
]

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

print("Selfbot running for games-chat...")

while True:
    try:
        # Randomly list se ek message select karein
        message_to_send = random.choice(MESSAGES)
        payload = {"content": message_to_send}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"[SUCCESS] Sent: {message_to_send}")
        elif response.status_code == 429:
            # Slowmode ya Rate limit handling
            retry_after = response.json().get('retry_after', 5)
            print(f"[RATE LIMITED] Waiting for {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"[ERROR] Status Code {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[EXCEPTION] {e}")

    # 2 minute delay (120 seconds)
    time.sleep(120)
