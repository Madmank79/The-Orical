import os
import time
import json
import requests
from datetime import datetime, timezone

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
API_KEY = os.environ.get("API_FOOTBALL_KEY")

LEAGUE_ID = 39          # Premier League
POLL_INTERVAL = 45      # seconds
STATE_FILE = "seen_goals.json"

HEADERS = {"x-apisports-key": API_KEY}

def load_seen():
    try:
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)

def send_goal(photo_url, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        print("Telegram response:", r.status_code)
    except Exception as e:
        print("Telegram error:", e)

def get_live_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    params = {"live": "all", "league": LEAGUE_ID}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    if r.status_code != 200:
        print("API error:", r.status_code, r.text[:300])
        return []
    return r.json().get("response", [])

def process_match(match, seen):
    fixture_id = match["fixture"]["id"]
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    home_score = match["goals"]["home"]
    away_score = match["goals"]["away"]

    events = match.get("events") or []
    for event in events:
        if event.get("type") != "Goal":
            continue

        minute = event.get("time", {}).get("elapsed")
        player = event.get("player", {})
        player_id = player.get("id")
        player_name = player.get("name") or "Unknown"
        team_name = event.get("team", {}).get("name") or ""

        goal_key = f"{fixture_id}-{minute}-{player_id}-{event.get('detail')}"

        if goal_key in seen:
            continue

        # New goal found
        seen.add(goal_key)

        photo = f"https://media.api-sports.io/football/players/{player_id}.png" if player_id else None

        caption = (
            f"⚽ **GOAL!**\n\n"
            f"**{player_name}** ({team_name})\n"
            f"{home} **{home_score} – {away_score}** {away}\n"
            f"{minute}'"
        )

        if photo:
            send_goal(photo, caption)
        else:
            # Fallback without photo
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": CHAT_ID,
                "text": caption,
                "parse_mode": "Markdown"
            }, timeout=15)

        print(f"New goal posted: {player_name} → {home} {home_score}-{away_score} {away}")

def main():
    if not all([TOKEN, CHAT_ID, API_KEY]):
        print("Missing one or more environment variables")
        return

    print("Premier League live goal watcher started...")
    seen = load_seen()

    while True:
        try:
            matches = get_live_matches()
            if matches:
                print(f"{datetime.now(timezone.utc).isoformat()} | {len(matches)} live match(es)")
                for match in matches:
                    process_match(match, seen)
                save_seen(seen)
            else:
                print(f"{datetime.now(timezone.utc).isoformat()} | No live PL matches")
        except Exception as e:
            print("Error in loop:", e)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
