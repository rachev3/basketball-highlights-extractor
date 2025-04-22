#!/usr/bin/env python3
# Play-by-Play Scraper for basketball.bg games

import argparse
import json
import re
import time
from typing import Dict, List, Optional, Tuple, Union

import requests
from bs4 import BeautifulSoup


class PlayByPlayScraper:
    """
    Scraper for play-by-play data from basketball.bg game pages.
    """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.base_url = f"https://comps.basketball.bg/game_play.inc.php?g_id={game_id}"
        self.events = []

    def fetch_html(self, url: str, max_retries: int = 3) -> str:
        """
        Fetch HTML from URL with retries on failure.
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Request failed: {e}. Retrying in 2 seconds...")
                time.sleep(2)
        
        # This should never happen due to the exception in the loop
        raise RuntimeError("Failed to fetch HTML after maximum retries")

    def parse_score(self, score_div) -> Tuple[int, int]:
        """
        Parse home and away scores from a score div.
        """
        if not score_div:
            return None, None
        
        spans = score_div.find_all("span")
        if len(spans) != 2:
            print(f"Warning: Expected 2 spans in score div, found {len(spans)}")
            return None, None
        
        try:
            home_score = int(spans[0].text.strip())
            away_score = int(spans[1].text.strip())
            return home_score, away_score
        except (ValueError, IndexError) as e:
            print(f"Failed to parse scores: {e}")
            return None, None

    def parse_event_row(self, row, quarter: str) -> Optional[Dict]:
        """
        Parse a single event row into a structured event object.
        """
        is_score = "tr_score" in row.get("class", [])
        
        # Extract time
        time_div = row.select_one("td.td_score div.time")
        if not time_div:
            # Some rows might be headers or empty
            return None
        
        time_str = time_div.text.strip()
        
        # Home and away cells
        home_cell = row.select_one("td.td_info.td_home")
        away_cell = row.select_one("td.td_info.td_away")
        
        # Determine which team has the event (home or away)
        home_info = home_cell.select_one("div.div_info") if home_cell else None
        away_info = away_cell.select_one("div.div_info") if away_cell else None
        
        if home_info:
            team = "home"
            info_div = home_info
        elif away_info:
            team = "away"
            info_div = away_info
        else:
            # No event information, skip this row
            return None
        
        # Extract player name if available
        player_link = info_div.select_one("a.player_name")
        player_name = player_link.text.strip() if player_link else None
        
        # Extract event text (full HTML content)
        event_text = str(info_div).strip()
        
        # Extract scores if this is a scoring event
        home_score, away_score = None, None
        if is_score:
            score_div = row.select_one("td.td_score div.score")
            if score_div:
                home_score, away_score = self.parse_score(score_div)
        
        return {
            "quarter": quarter,
            "time": time_str,
            "team": team,
            "player_name": player_name,
            "event_text": event_text,
            "home_score": home_score,
            "away_score": away_score
        }

    def parse_quarter_table(self, soup, quarter_id: str) -> List[Dict]:
        """
        Parse all events in a quarter table.
        """
        quarter_events = []
        
        # Convert quarter_id (like "q_1") to quarter name (like "Q1")
        match = re.match(r"q_(\d+|OT\d*)", quarter_id)
        if not match:
            print(f"Warning: Invalid quarter ID format: {quarter_id}")
            return []
        
        quarter_str = match.group(1)
        if quarter_str.isdigit():
            quarter_name = f"Q{quarter_str}"
        else:  # Handle overtime periods
            quarter_name = quarter_str
        
        # Find the quarter table
        table = soup.select_one(f"table.tbl_play#{quarter_id}")
        if not table:
            print(f"Warning: Table for quarter {quarter_id} not found")
            return []
        
        # Process each row in the table
        for row in table.find_all("tr"):
            event = self.parse_event_row(row, quarter_name)
            if event:
                quarter_events.append(event)
        
        return quarter_events

    def scrape(self) -> List[Dict]:
        """
        Scrape play-by-play data for all quarters.
        """
        # Fetch the main page HTML
        html = self.fetch_html(self.base_url)
        soup = BeautifulSoup(html, "html.parser")
        
        # Find all quarter tables (regular quarters + overtimes)
        quarter_tables = soup.select("table.tbl_play[id^='q_']")
        
        if not quarter_tables:
            raise ValueError("No quarter tables found on the page. The page structure may have changed.")
        
        # Extract quarter IDs
        quarter_ids = [table.get("id") for table in quarter_tables if table.get("id")]
        
        # Process each quarter
        for quarter_id in quarter_ids:
            quarter_events = self.parse_quarter_table(soup, quarter_id)
            self.events.extend(quarter_events)
        
        return self.events

    def save_json(self, filename: Optional[str] = None) -> str:
        """
        Save events to a JSON file.
        """
        if not filename:
            filename = f"pbp_{self.game_id}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(self.events)} events to {filename}")
        return filename

    def save_csv(self, filename: Optional[str] = None) -> str:
        """
        Save events to a CSV file.
        """
        if not filename:
            filename = f"pbp_{self.game_id}.csv"
        
        import csv
        
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=["quarter", "time", "team", "player_name", "event_text", "home_score", "away_score"]
            )
            writer.writeheader()
            writer.writerows(self.events)
        
        print(f"Saved {len(self.events)} events to {filename}")
        return filename


def main():
    parser = argparse.ArgumentParser(description="Scrape play-by-play data from basketball.bg games")
    parser.add_argument("--game_id", required=True, help="Game ID to scrape")
    parser.add_argument("--output", choices=["json", "csv"], default="json", help="Output format (json or csv)")
    parser.add_argument("--output_file", help="Custom output filename")
    
    args = parser.parse_args()
    
    scraper = PlayByPlayScraper(args.game_id)
    events = scraper.scrape()
    
    if args.output == "json":
        scraper.save_json(args.output_file)
    else:
        scraper.save_csv(args.output_file)


if __name__ == "__main__":
    main() 