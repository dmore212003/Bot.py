import asyncio
import requests
import telegram

TELEGRAM_TOKEN = "8808593549:AAHn7yZ36EPAvBvwMQz_Ceu21UYvHvILuv8"
CHAT_ID = "8709943285"

SPORTY_API_URL = "https://sportybet.com" 
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def fetch_virtual_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://sportybet.com",
        "Referer": "https://sportybet.com/"
    }
    try:
        response = requests.get(SPORTY_API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(f"SportyBet server error code: {response.status_code}")
        return None
    except Exception as e:
        print(f"Connection network failure: {e}")
        return None

def analyze_predictions(data):
    if not data or not isinstance(data, dict) or "data" not in data:
        return ["⏳ Waiting for SportyBet live virtual data..."]
    
    fixtures = data.get("data", {}).get("fixtures", [])[:3]
    if not fixtures:
        return ["⚽ Live virtual round updating. Waiting for new matches..."]
        
    return [f"🔥 Over 1.5 Pick: {m.get('homeTeamName', 'Home')} vs {m.get('awayTeamName', 'Away')}" for m in fixtures]

async def main():
    print("Bot started successfully on the cloud server...")
    while True:
        raw_data = fetch_virtual_data()
        game_tips = analyze_predictions(raw_data)
        if game_tips:
            message_text = "⚽ **SPORTYBET VIRTUAL TIPS** ⚽\n\n" + "\n".join(game_tips)
            try:
                await bot.send_message(chat_id=CHAT_ID, text=message_text, parse_mode="Markdown")
                print("Prediction successfully sent to Telegram!")
            except Exception as e:
                print(f"Telegram failed. Error: {e}")
        await asyncio.sleep(180)

if __name__ == "__main__":
    asyncio.run(main())
  
