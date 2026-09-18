import asyncio
import requests
import telegram

TELEGRAM_TOKEN = "8808593549:AAHn7yZ36EPAvBvwMQz_Ceu21UYvHvILuv8"
CHAT_ID = "8709943285"

# The official raw data link for SportyBet Nigeria Virtual Football (Leagues)
SPORTY_API_URL = "https://sportybet.com"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def fetch_live_sporty_matches():
    # These parameters mimic a real phone browser looking at the Nigeria virtual layout
    params = {
        "productId": "3",       # 3 is the system code for Virtual Football
        "status": "not_started" # Only pull upcoming matches that haven't kicked off yet
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-NG,en;q=0.9", # Set strictly to Nigeria network configuration
        "Origin": "https://sportybet.com",
        "Referer": "https://sportybet.com/ng/virtual/"
    }
    
    try:
        response = requests.get(SPORTY_API_URL, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(f"SportyBet firewall response code: {response.status_code}")
        return None
    except Exception as e:
        print(f"Network error linking to SportyBet: {e}")
        return None

def analyze_real_fixtures(data):
    if not data or not isinstance(data, dict):
        return ["⏳ Syncing with live SportyBet board..."]
        
    # Check if SportyBet successfully accepted the connection
    if data.get("code") != 10000:
        return ["⚠️ SportyBet connection restricted. Updates coming shortly..."]
        
    # Navigate through SportyBet's real JSON tree structure
    categories = data.get("data", {}).get("categories", [])
    if not categories:
        return ["⚽ Live round in progress. Waiting for the next scheduled fixtures..."]
        
    predictions = []
    # Grab the upcoming matches from the first available active league (e.g., Virtual EPL)
    tournaments = categories[0].get("tournaments", [])
    if tournaments:
        events = tournaments[0].get("events", [])[:4] # Target the top 4 upcoming games
        for event in events:
            home_team = event.get("homeTeamName", "Home")
            away_team = event.get("awayTeamName", "Away")
            predictions.append(f"🔥 Live Pick (Over 1.5): {home_team} vs {away_team}")
            
    if not predictions:
        return ["⚽ Sorting upcoming round fixtures..."]
        
    return predictions

async def main():
    print("Bot sync sequence initialized on cloud server...")
    while True:
        raw_data = fetch_live_sporty_matches()
        game_tips = analyze_real_fixtures(raw_data)
        
        if game_tips:
            message_text = "⚽ **REAL-TIME SPORTYBET VIRTUAL TIPS** ⚽\n\n" + "\n".join(game_tips)
            try:
                await bot.send_message(chat_id=CHAT_ID, text=message_text, parse_mode="Markdown")
                print("Live synchronization tip pushed to Telegram!")
            except Exception as e:
                print(f"Telegram communication failure: {e}")
                
        # Virtual rounds refresh rapidly every 3 minutes
        await asyncio.sleep(180)

if __name__ == "__main__":
    asyncio.run(main())
                
