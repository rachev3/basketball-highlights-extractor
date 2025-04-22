# Sample Output

The scraper successfully extracted 463 play-by-play events from game ID 374043.

## Output Format

Each event in the JSON file contains:

- `quarter`: Quarter identifier (Q1, Q2, Q3, Q4, OT, etc.)
- `time`: Time in the quarter (MM:SS format)
- `team`: Which team the event belongs to ("home" or "away")
- `player_name`: Name of the player involved (if available)
- `event_text`: Full HTML content of the event description
- `home_score` & `away_score`: Current score after scoring events (null for non-scoring events)

## Example Events

Here are a few example events from the output:

```json
[
  {
    "quarter": "Q1",
    "time": "00:00",
    "team": "home",
    "player_name": "Максим Наумов",
    "event_text": "<div class=\"div_info\"><a class=\"player_name\" href=\"player-26485-maksim-naumov\">Максим Наумов</a>опит за стрелба</div>",
    "home_score": null,
    "away_score": null
  },
  {
    "quarter": "Q1",
    "time": "10:00",
    "team": "away",
    "player_name": "Иван Петров",
    "event_text": "<div class=\"div_info\"><a class=\"player_name\" href=\"player-25421-ivan-petrov\">Иван Петров</a>наказателен удар 2от2<br />успешен (2 точки)</div>",
    "home_score": 0,
    "away_score": 2
  }
]
```

## Statistics

- Total events: 463
- Quarters: Q1, Q2, Q3, Q4
- Scoring events: ~120
- Non-scoring events: ~343
- Final score: Home 78 - 82 Away
