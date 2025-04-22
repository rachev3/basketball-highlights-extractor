# Play-by-Play Scraper

A scraper for extracting play-by-play event data from basketball.bg game pages.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper with a game ID:

```bash
python scraper.py --game_id 374043
```

### Options

- `--game_id`: (Required) The game ID to scrape (from basketball.bg)
- `--output`: Output format - `json` (default) or `csv`
- `--output_file`: Custom output filename (default: `pbp_<game_id>.<json|csv>`)

## Example

Scrape a game and output to JSON:

```bash
python scraper.py --game_id 374043
```

Scrape a game and output to CSV:

```bash
python scraper.py --game_id 374043 --output csv
```

## Notes

- The scraper handles all quarters, including overtime periods.
- Event text is preserved in its original format, including HTML.
- Scoring events include the updated score.
- The scraper implements retry logic for handling transient network errors.
