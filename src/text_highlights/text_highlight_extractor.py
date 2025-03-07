#!/usr/bin/env python3
"""
Basketball Text Highlights Generator

This script scrapes basketball game data and generates text-based highlight summaries
including time, score, quarter, and a brief description of the event.

Assignment 3 Implementation
"""

import argparse
import json
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup


class TextHighlightExtractor:
    """
    A class to scrape basketball game data and generate text highlights.
    This is separate from the audio-based highlight extraction and focuses solely
    on generating text descriptions of key game moments.
    """

    def __init__(self, url, output_format="text", output_file=None):
        """
        Initialize the text highlight extractor.
        
        Args:
            url (str): URL of the basketball game page containing play-by-play data
            output_format (str): Format for output ('text', 'json', or 'csv')
            output_file (str): Path to save the highlights (if None, prints to console)
        """
        self.url = url
        self.output_format = output_format
        self.output_file = output_file
        self.play_by_play_data = []
        self.box_score_data = {}
        self.highlights = []
    
    def scrape_play_by_play(self):
        """
        Scrape the play-by-play data from the game page.
        
        Returns:
            list: List of play-by-play events with quarter, time, score, and description
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This will need to be adjusted based on the actual HTML structure of the target site
            play_by_play_table = soup.find('table', {'id': 'play-by-play'})
            
            if not play_by_play_table:
                print("Could not find play-by-play data on the page")
                return []
            
            events = []
            current_quarter = "Q1"
            
            for row in play_by_play_table.find_all('tr'):
                # Skip header rows
                if row.find('th'):
                    continue
                
                # Find all cells in the row
                cells = row.find_all('td')
                
                # Skip rows without enough cells
                if len(cells) < 3:
                    continue
                
                # Extract quarter information if present
                quarter_text = cells[0].get_text().strip()
                if quarter_text and re.match(r'Q\d|OT\d?', quarter_text):
                    current_quarter = quarter_text
                    continue
                
                # Extract time, description, and score
                time_str = cells[0].get_text().strip()
                description = cells[1].get_text().strip()
                score_text = cells[2].get_text().strip()
                
                # Skip rows without valid time format
                if not re.match(r'\d{2}:\d{2}', time_str):
                    continue
                
                # Parse score (e.g., "76-72")
                score_match = re.search(r'(\d+)[^\d]+(\d+)', score_text)
                if score_match:
                    home_score = int(score_match.group(1))
                    away_score = int(score_match.group(2))
                    score = f"{home_score}–{away_score}"
                else:
                    score = "N/A"
                
                events.append({
                    'quarter': current_quarter,
                    'time': time_str,
                    'description': description,
                    'score': score,
                    'home_score': home_score if score_match else None,
                    'away_score': away_score if score_match else None
                })
            
            self.play_by_play_data = events
            return events
            
        except requests.exceptions.RequestException as e:
            print(f"Error scraping play-by-play data: {e}")
            return []
    
    def scrape_box_score(self):
        """
        Scrape the box score data from the game page (optional, for advanced highlight logic).
        
        Returns:
            dict: Dictionary containing player statistics
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This will need to be adjusted based on the actual HTML structure
            box_score_tables = soup.find_all('table', {'class': 'box-score'})
            
            box_score = {
                'home_team': {'players': []},
                'away_team': {'players': []}
            }
            
            if not box_score_tables or len(box_score_tables) < 2:
                print("Could not find box score data on the page")
                return box_score
            
            # Extract team names
            team_headers = soup.find_all('h2', {'class': 'team-name'})
            if len(team_headers) >= 2:
                box_score['away_team']['name'] = team_headers[0].get_text().strip()
                box_score['home_team']['name'] = team_headers[1].get_text().strip()
            
            # Process each team's box score
            for i, table in enumerate(box_score_tables[:2]):
                team_key = 'away_team' if i == 0 else 'home_team'
                
                for row in table.find_all('tr'):
                    if row.find('th'):  # Skip header rows
                        continue
                    
                    cells = row.find_all('td')
                    if len(cells) < 8:  # Minimum columns for player stats
                        continue
                    
                    player_name = cells[0].get_text().strip()
                    points = int(cells[-1].get_text().strip() or 0)
                    rebounds = int(cells[-3].get_text().strip() or 0)
                    assists = int(cells[-4].get_text().strip() or 0)
                    
                    box_score[team_key]['players'].append({
                        'name': player_name,
                        'points': points,
                        'rebounds': rebounds,
                        'assists': assists
                    })
            
            self.box_score_data = box_score
            return box_score
            
        except requests.exceptions.RequestException as e:
            print(f"Error scraping box score data: {e}")
            return {'home_team': {'players': []}, 'away_team': {'players': []}}
    
    def extract_highlights(self):
        """
        Extract highlights from the play-by-play data based on defined criteria.
        
        Returns:
            list: List of highlight events
        """
        if not self.play_by_play_data:
            print("No play-by-play data available. Call scrape_play_by_play() first.")
            return []
        
        highlights = []
        
        # Track score progression for lead changes and runs
        previous_lead_team = None
        current_run = {'team': None, 'points': 0}
        
        # Process all events chronologically
        for i, event in enumerate(self.play_by_play_data):
            is_highlight = False
            highlight_reason = []
            
            # Skip events without score
            if event['home_score'] is None or event['away_score'] is None:
                continue
            
            # Determine current leading team
            if event['home_score'] > event['away_score']:
                current_lead_team = 'home'
            elif event['away_score'] > event['home_score']:
                current_lead_team = 'away'
            else:
                current_lead_team = 'tie'
            
            # Check for lead change
            if previous_lead_team and current_lead_team != previous_lead_team and current_lead_team != 'tie':
                is_highlight = True
                highlight_reason.append("Lead change")
            
            # Check for clutch plays in final minutes
            if event['quarter'] in ['Q4', 'OT', 'OT1', 'OT2', 'OT3']:
                minutes = int(event['time'].split(':')[0])
                if minutes < 2:  # Final 2 minutes
                    score_diff = abs(event['home_score'] - event['away_score'])
                    if score_diff <= 5:  # Close game (within 5 points)
                        if "made" in event['description'].lower() or "3pt" in event['description'].lower():
                            is_highlight = True
                            highlight_reason.append("Clutch play")
            
            # Check for buzzer-beaters
            if event['time'] == '00:00' or event['time'] == '0:00':
                if "made" in event['description'].lower():
                    is_highlight = True
                    highlight_reason.append("Buzzer-beater")
            
            # Track scoring runs
            if "made" in event['description'].lower():
                # Determine which team scored
                scoring_team = 'unknown'
                if i > 0 and self.play_by_play_data[i-1]['home_score'] != event['home_score']:
                    scoring_team = 'home'
                elif i > 0 and self.play_by_play_data[i-1]['away_score'] != event['away_score']:
                    scoring_team = 'away'
                
                # Update or reset current run
                if current_run['team'] == scoring_team:
                    if "3pt" in event['description'].lower():
                        current_run['points'] += 3
                    elif "free throw" in event['description'].lower():
                        current_run['points'] += 1
                    else:
                        current_run['points'] += 2
                else:
                    current_run = {'team': scoring_team, 'points': 0}
                    if "3pt" in event['description'].lower():
                        current_run['points'] = 3
                    elif "free throw" in event['description'].lower():
                        current_run['points'] = 1
                    else:
                        current_run['points'] = 2
                
                # Check if this is a significant run
                if current_run['points'] >= 8:
                    is_highlight = True
                    highlight_reason.append(f"{current_run['points']}-0 run")
            
            # If this event is a highlight, add it to our list
            if is_highlight:
                highlights.append({
                    'quarter': event['quarter'],
                    'time': event['time'],
                    'score': event['score'],
                    'description': event['description'],
                    'reason': ", ".join(highlight_reason)
                })
            
            # Update previous lead team for next iteration
            previous_lead_team = current_lead_team
        
        self.highlights = highlights
        return highlights
    
    def format_highlights(self):
        """
        Format the highlights according to the specified output format.
        
        Returns:
            str or dict: Formatted highlights
        """
        if not self.highlights:
            return "No highlights found."
        
        if self.output_format == 'json':
            return json.dumps(self.highlights, indent=2)
        
        elif self.output_format == 'csv':
            header = "Quarter,Time,Score,Description,Reason\n"
            rows = []
            for h in self.highlights:
                # Escape commas and quotes in the description
                safe_desc = f'"{h["description"].replace("\"", "\"\"")}"'
                rows.append(f"{h['quarter']},{h['time']},{h['score']},{safe_desc},{h['reason']}")
            return header + "\n".join(rows)
        
        else:  # Default to text format
            output = []
            for h in self.highlights:
                output.append(f"[{h['quarter']} - {h['time']}] Score: {h['score']}")
                output.append(f"{h['description']}")
                output.append(f"Highlight reason: {h['reason']}")
                output.append("-" * 40)
            return "\n".join(output)
    
    def save_or_print_highlights(self):
        """
        Save highlights to a file or print them to the console.
        """
        formatted_highlights = self.format_highlights()
        
        if self.output_file:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_highlights)
            print(f"Highlights saved to {self.output_file}")
        else:
            print("\n==== BASKETBALL GAME HIGHLIGHTS ====\n")
            print(formatted_highlights)
    
    def run(self):
        """
        Run the complete text highlight extraction pipeline.
        """
        print(f"Scraping play-by-play data from {self.url}...")
        self.scrape_play_by_play()
        
        print(f"Scraping box score data from {self.url}...")
        self.scrape_box_score()
        
        print("Extracting highlights based on criteria...")
        self.extract_highlights()
        
        print(f"Found {len(self.highlights)} highlights.")
        self.save_or_print_highlights()
        
        return self.highlights


def main():
    """
    Parse command line arguments and run the text highlight extractor.
    """
    parser = argparse.ArgumentParser(description='Basketball Text Highlights Generator')
    parser.add_argument('url', help='URL of the basketball game page containing play-by-play data')
    parser.add_argument('--output-format', choices=['text', 'json', 'csv'], default='text',
                        help='Format for highlight output (default: text)')
    parser.add_argument('--output-file', help='Path to save the highlights (if not specified, prints to console)')
    
    args = parser.parse_args()
    
    extractor = TextHighlightExtractor(
        url=args.url,
        output_format=args.output_format,
        output_file=args.output_file
    )
    
    extractor.run()


if __name__ == "__main__":
    main() 