import time
import json
import os
import requests
from bs4 import BeautifulSoup

def probe_leagues_and_seasons(min_league, max_league, min_season, max_season, interval_seconds, output_file):
    results = []

    for league_id in range(min_league, max_league + 1):
        league_data = {"league": league_id, "seasons": set()}
        for season_id in range(min_season, max_season + 1):
            url = f"https://stats.sharksice.timetoscore.com/display-schedule.php?stat_class=1&league={league_id}&season={season_id}"
            print(f"Probing URL: {url}")

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                schedule_html = response.text

                # Parse the schedule page to find all game links
                soup = BeautifulSoup(schedule_html, "html.parser")
                tables = soup.find_all('table')
                top_level_tables = [table for table in tables if table.find_parent('table') is None]

                if len(top_level_tables) > 0:
                    print(f"Data found for league {league_id}, season {season_id}")
                    league_data["seasons"].add(season_id)

                    # Save the fetched HTML to a subfolder
                    folder_path = os.path.join("schedules", f"league={league_id}", f"season={season_id}")
                    os.makedirs(folder_path, exist_ok=True)
                    with open(os.path.join(folder_path, "schedule.html"), "w") as f:
                        f.write(schedule_html)
                else:
                    print(f"No data for league {league_id}, season {season_id}")
            except Exception as e:
                print(f"Error probing URL {url}: {e}")

            # Wait for the specified interval before the next request
            time.sleep(interval_seconds)

        if league_data["seasons"]:
            league_data["seasons"] = list(league_data["seasons"])  # Convert set to list for JSON serialization
            results.append(league_data)

    # Save results to a JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

# Example usage
probe_leagues_and_seasons(min_league=1, max_league=70, min_season=1, max_season=70, interval_seconds=9, output_file="leagues_seasons_2_70_1_70.json")
