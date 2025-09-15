#! /usr/bin/env python
import requests
from datetime import date, timedelta


def get_last_game_results(days_back=1):
    # Calculate target date
    target = date.today() - timedelta(days=days_back)
    date_str = target.isoformat()  # 'YYYY-MM-DD'

    url = (
        "https://statsapi.mlb.com/api/v1/schedule"
        f"?sportId=1&startDate={date_str}&endDate={date_str}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def main():
    data = get_last_game_results(days_back=1)
    dates = data.get("dates", [])

    if not dates:
        print("No games were played on that date.")
        return

    print(f"=== MLB Game Results for {date.today() - timedelta(days=1)} ===")
    for day in dates:
        games = day.get("games", [])
        for g in games:
            home = g["teams"]["home"]["team"]["name"]
            away = g["teams"]["away"]["team"]["name"]
            home_runs = g["teams"]["home"]["score"]
            away_runs = g["teams"]["away"]["score"]
            status = g["status"]["detailedState"]

            if status.lower() in ("final", "final/ot", "game over"):
                print(f"{away} {away_runs} @ {home} {home_runs} – {status}")
            else:
                # If the game isn't final (like delayed, postponed), show status
                print(f"{away} @ {home} – Status: {status}")


if __name__ == "__main__":
    main()
