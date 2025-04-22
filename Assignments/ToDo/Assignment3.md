# Assignment: Data Scraping & Text-Only Highlight Extraction

## Objective

Scrape basketball game data (statistics, play-by-play, etc.) from the provided links and generate a **textual highlights** summary. Each highlight should include the **time**, **score**, **quarter**, and a **brief description** of the event.  
**Important:** We do **not** need to store data in a database—just parse, analyze, and output the highlights.

## Scope

- **Data Sources:** Official match pages containing:
  - **Box Score** (player points, rebounds, assists, etc.).
  - **Play-by-Play** events (scoring actions, fouls, turnovers, etc.).
  - **Additional Stats** like shot charts or scoring progressions (optional).
- **Output:**
  - A text-based list of highlights, each with:
    - Quarter (e.g., Q1, Q2, Q3, Q4, OT)
    - Time in quarter (e.g., 02:49)
    - Score at that moment (e.g., 79–84)
    - Short description (e.g., “Player X hits a clutch 3-pointer”)

## Requirements

1. **Scraping the Data**

   - **Play-by-Play (PBP):**
     - Capture each event’s quarter, time, description (e.g., “3pt jump shot made,” “Foul,” etc.), and score updates.
   - **Box Score (Optional for Highlights):**
     - Parse each player’s basic stats (points, rebounds, assists). We might incorporate this later for advanced highlight logic.
   - **No Database:**
     - Store the scraped data in memory (e.g., Python lists/dicts) or export to a lightweight format like JSON/CSV, but **do not** set up a database.

2. **Highlight Extraction Logic (Text Only)**

   - **Initial Criteria (Examples):**
     - **Lead changes** (when one team overtakes the other).
     - **Clutch plays** in the final minutes (e.g., tying the game or taking the lead).
     - **Buzzer-beaters** at the end of any quarter.
     - **Significant scoring runs** (e.g., an 8–0 run).
   - Output a concise text entry for each highlight.

3. **Implementation Details**

   - **Language & Libraries:**
     - Python recommended, using **Requests** or **httpx** for HTTP requests, and **BeautifulSoup** or **lxml** for HTML parsing.
   - **Data Structures:**
     - In-memory Python lists/dicts, or a single JSON file to hold the scraped results.
   - **Workflow Example:**
     1. Scrape PBP data → store each event (quarter, time, old_score, new_score, description).
     2. Apply highlight criteria to the event list → identify which events qualify.
     3. Print or save a text-based summary of those highlight events.

4. **Textual Output of Highlights**

   - A straightforward approach could be printing lines like:
     ```
     [Q4 - 01:05] Score: 77–79
     Big 3-pointer by #7 to give the team a 2-point lead
     ```
   - Or store them in a structured text file (CSV, JSON, or even Markdown).

5. **Testing & Validation**
   - Use sample matches to confirm:
     - The scraper consistently fetches all events in chronological order.
     - The highlight criteria capture the correct moments.
   - Check edge cases like overtime, missing data, or unusual scoring runs.

## Deliverables

1. **Scraper Script:**
   - A Python script (or set of scripts) that fetches the PBP and box score data from the target URL(s).
   - Stores or returns the data in memory for processing.
2. **Highlight Extraction Module:**
   - A function or class that implements the highlight logic on the scraped data.
   - Produces a text-based summary (console output, .txt file, or similar).
3. **Documentation:**
   - A short README explaining:
     - How to install and run the scraper.
     - How to adjust or extend the highlight criteria.
     - Any known limitations (e.g., missing data fields).
4. **Sample Output:**
   - Provide an example of the final highlight list for a single match, demonstrating the logic in action.

## Evaluation Criteria

- **Completeness of Data:** Does the script reliably scrape all relevant play-by-play events?
- **Highlight Accuracy:** Do the identified highlights match the specified criteria (lead changes, clutch plays, etc.)?
- **Code Quality & Maintainability:** Is the code modular, well-documented, and easy to adapt for new criteria?
- **Documentation:** Is the README clear on how to run the scraper and interpret results?

---

**Note to Devs:**  
Focus on accurate data scraping and a straightforward highlight logic. We’ll expand on advanced features (like video alignment or advanced stats usage) later. For now, simply reading the data, identifying the highlights, and outputting them in text form is sufficient.
