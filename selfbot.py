import time
import random
import requests

# 1. Alt Account ka Fresh User Token (Network Tab se Copy Kiya Hua)
USER_TOKEN = "MTU1NzY5NzY1OTYzNTI0MDk2Mg.G1Axrt.yohF_tqIhTXmTbyHTHIKkUvmcrdR7o8lehUH8A"

# 2. Goat Funded Trader ke Mini-Game Channel ki ID
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

# Note: User Token ke saath "Bot " nahi lagaya jata
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
            
            # Anti-Ban Safety Delay: Random gap between 360 to 600 seconds (6 to 10 mins)
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