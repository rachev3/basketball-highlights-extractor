# Implementation Notes

## Architecture Decision

The scraper follows an object-oriented design with a `PlayByPlayScraper` class that handles:

1. Fetching HTML from the target URL
2. Parsing quarter tables and individual event rows
3. Extracting structured data from each event
4. Saving the results in JSON or CSV format

## Technical Challenges

### HTML Structure

The basketball.bg website structures play-by-play data in quarter-specific tables with rows for each event. We handle this by:

- Identifying tables by their `id="q_1"`, `id="q_2"`, etc. attributes
- Processing each row to extract team, player, event description, and score information
- Converting quarter identifiers from `q_1` to `Q1` for better readability

### Scoring Events

Scoring events are marked with `tr_score` class and contain updated score information. We:

- Check for the presence of this class to identify scoring events
- Extract home and away scores from the spans within the score div
- Set scores to `null` for non-scoring events

### Character Encoding

The site uses Cyrillic characters for player names and event descriptions. We ensure proper handling by:

- Setting UTF-8 encoding when writing output files
- Using `ensure_ascii=False` when encoding JSON to preserve original characters

### Error Handling

To ensure robustness, the scraper:

- Retries HTTP requests on transient failures
- Logs warnings for unexpected HTML structures
- Gracefully handles missing data fields
- Provides clear error messages if the page structure changes

## Testing

The scraper was tested on the example game ID 374043, successfully extracting 463 events across all quarters. Testing included:

- Verifying proper extraction of all quarters (Q1, Q2, Q3, Q4)
- Confirming correct parsing of scoring and non-scoring events
- Validating the output JSON and CSV formats
- Checking that all required fields are properly populated
