# Basketball Text Highlights Generator

This module scrapes basketball game data from web pages and generates text-based highlight summaries. Each highlight includes the time, score, quarter, and a brief description of the event.

## Assignment 3 Implementation

This is an implementation of Assignment 3: Data Scraping & Text-Only Highlight Extraction. The module operates independently from the existing video-based highlight extraction system.

## Features

- Scrapes play-by-play data from basketball game pages
- Optionally scrapes box score data for advanced highlight logic
- Identifies key game moments based on highlight criteria:
  - Lead changes
  - Clutch plays in final minutes
  - Buzzer-beaters
  - Significant scoring runs (8-0 or more)
- Outputs highlights in multiple formats (text, JSON, CSV)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements_text_highlights.txt
```

This will install:

- requests: For making HTTP requests
- beautifulsoup4: For parsing HTML
- lxml: A faster HTML parser for BeautifulSoup

## Usage

### From the Command Line

```bash
python text_highlight_extractor.py "https://example.com/basketball/game/12345/play-by-play" --output-format json --output-file highlights.json
```

Parameters:

- URL (required): The URL of the basketball game page containing play-by-play data
- `--output-format`: Format for the highlights (text, json, or csv). Default is text.
- `--output-file`: Path to save the highlights. If not specified, prints to console.

### As a Module

```python
from text_highlight_extractor import TextHighlightExtractor

# Initialize the extractor
extractor = TextHighlightExtractor(
    url="https://example.com/basketball/game/12345/play-by-play",
    output_format="text",
    output_file="highlights.txt"
)

# Run the extraction pipeline
highlights = extractor.run()

# Or run the steps individually
extractor.scrape_play_by_play()
extractor.scrape_box_score()  # Optional
extractor.extract_highlights()
extractor.save_or_print_highlights()
```

## Customizing Highlight Criteria

The highlight extraction logic is contained in the `extract_highlights()` method of the `TextHighlightExtractor` class. You can modify this method to adjust or extend the criteria for what constitutes a highlight.

Current highlight criteria:

1. **Lead changes**: When one team overtakes the other
2. **Clutch plays**: In the final 2 minutes of Q4 or overtime, in close games (within 5 points)
3. **Buzzer-beaters**: Shots made at the end of any quarter
4. **Scoring runs**: When a team scores 8 or more consecutive points

## Sample Output

Text format example:

```
[Q4 - 01:05] Score: 77–79
Johnson hits a 3-pointer from the corner
Highlight reason: Lead change, Clutch play

[Q2 - 00:00] Score: 45–43
Williams makes a half-court shot at the buzzer
Highlight reason: Buzzer-beater
```

## Known Limitations

1. The HTML parsing is based on generic table structures. You may need to adjust the selectors based on the specific website you're scraping.
2. Lead changes and scoring runs detection requires complete play-by-play data with accurate scores.
3. The scraper doesn't handle dynamic content loaded via JavaScript. For such websites, you might need to use Selenium or a similar tool.

## Future Enhancements

- Add team name detection to improve highlight descriptions
- Implement more advanced highlight criteria using player stats
- Create a configurable criteria system to easily adjust highlight definitions
- Add support for scraping from multiple data sources/websites

## License

This project is open source and available under the MIT License.
