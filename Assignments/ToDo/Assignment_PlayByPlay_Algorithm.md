# Assignment: Highlight Extraction Algorithm

## 1. Overview

Our objective is to develop an **algorithm** (not the scraping process) that analyzes structured play-by-play data from basketball matches and automatically extracts the **top 10 match highlights**. Each highlight must include:

1. **Clock Time:** The time remaining (or elapsed) in the period when the event occurred (e.g., “00:05”).
2. **Period/Quarter:** Which quarter (or overtime period) the event happened in (e.g., “P4”).
3. **Score:** The game score at the moment of the event (e.g., “50–57”).
4. **Highlight Explanation:** A concise statement of why the event is significant.

Because the site we are scraping does **not** provide additional context tags like “clutch,” the algorithm must infer significance from the event’s type, the score difference, the period/time, and other available data fields.

---

## 2. Input Data Specifications

We will receive already scraped play-by-play events. Each event typically contains:

- **Clock (Time):** For example, `"00:05"` (time left in the quarter).
- **Period:** For example, `"P4"` (4th quarter), or `"OT"` (overtime).
- **Score:** For example, `"50-57"`.
- **Event Description:** A textual description that can include:
  - Player name (e.g., “Иван Маринов”)
  - Action type (e.g., “3pt jump shot made,” “free throw 1 of 2 missed,” “turnover - ball handling,” etc.)
  - Possibly some short detail about the action, but **no extra “clutch” or “key shot” flags** are provided.

These events appear in chronological order (reverse chronological in the screenshots, but we can reorder as needed).

---

## 3. Algorithm Design Requirements

### 3.1. Event Parsing and Normalization

1. **Parsing:** Convert the raw data into a structured format (e.g., a list of objects or dictionaries). Each record should have standardized keys for time, period, score, event type, and so on.
2. **Normalization:**
   - Convert clock time into a uniform representation if needed (e.g., seconds from the start of the quarter).
   - Standardize period labels (`"P1"`, `"P2"`, `"P3"`, `"P4"`, `"OT"`) so the algorithm can compare them.

### 3.2. Event Categorization

Since we do not have explicit tags like “clutch,” we rely on:

- **Action Type:** Shots (2pt, 3pt, free throw), rebounds, turnovers, fouls, etc.
- **Score Change:** Identify events that increase or decrease the lead (e.g., made shots, missed shots, or free throws).
- **Period/Time:** Late-game events may be more significant, especially if the score is close.

We should define a **weighting system** for each category of event. For instance:

- **Made 3pt Shots:** Typically get higher weight than 2pt shots, especially if they significantly change the lead.
- **Free Throws:** Weight them less than field goals unless they happen in the last moments or break a tie.
- **Turnovers, Steals, Blocks:** Potentially high impact if the score is close or the turnover leads to a major momentum shift.
- **Rebounds:** Usually routine, but an offensive rebound at a critical time might be more impactful.
- **Fouls:** Might be noteworthy if it’s an unsportsmanlike or if free throws ensue at a tight score.

### 3.3. Scoring/Ranking Logic

Each event should get an **impact score** based on:

1. **Event Type Weight** – e.g., a 3pt made shot has a higher base weight than a routine defensive rebound.
2. **Score Differential Factor** – The difference between the teams’ scores before and after the event. Large swings or a close score might raise the impact.
3. **Time Factor** – Events that happen in the last minute of the 4th quarter (or OT) can be given extra importance.
4. **Lead/Trail Context** – Shots that tie the game, take the lead, or push a lead into double digits might receive higher weight.

### 3.4. Filtering and Highlight Selection

1. **Filter Out Low-Value Events:** If an event has an impact score below a certain threshold (e.g., a normal defensive rebound in the first minute when the score difference is large), we might exclude it.
2. **Sort Events by Impact Score:** Once all events have an assigned score, sort them in descending order.
3. **Select the Top 10:** Return the highest-scoring 10 events as the official highlights.

### 3.5. Output Format

The algorithm’s output for each highlight should contain:

- **Time:** The event clock (e.g., “00:05”).
- **Period:** The quarter/overtime (e.g., “P4”).
- **Score:** The scoreboard at that moment (e.g., “50–57”).
- **Highlight Explanation:** A short textual summary, e.g., “Иван Маринов, free throw 2 of 2 made — lead by 7.”

The final result can be a list or array of 10 highlight objects, ready for display.

---

## 4. Detailed Processing Flow

Below is a step-by-step outline (no code, just conceptual steps):

1. **Load the scraped data** into a structure that you can iterate over (already parsed from HTML).
2. **Standardize each record**:
   - Ensure the “time” field is consistent (e.g., “00:05” => 5 seconds left).
   - Parse the “score” string into numeric values for each team.
   - Identify the “event type” (e.g., 3pt shot, turnover, rebound) from the text description.
3. **Compute an impact score** for each event. Example approach:
   - Start with a **base value** depending on event type (e.g., 3 for a 3pt shot, 2 for a 2pt shot, 1 for a free throw).
   - Add or subtract points based on **score differential** or closeness of the game.
   - Multiply by a **time factor** if the event occurs late in the game or in a key moment.
4. **Filter out** events below a certain threshold.
5. **Sort the remaining events** by their impact scores in descending order.
6. **Pick the top 10** as the highlights.
7. **Generate a short explanation** for each highlight. Since the text is minimal (e.g., “3pt jump shot made”), the explanation can incorporate the event type, player name, and updated lead/trail context.
8. **Output** the highlights in a final structure or data file.

---

## 5. Additional Notes

- **No Extra Context:** Since the website’s data does not label anything as “clutch,” we must rely on the combination of event type, time, and score difference to infer significance.
- **Multiple OverTimes:** If the match extends into additional overtimes, treat them similarly to a “P5,” “P6,” etc., or label them “OT1,” “OT2.” The weighting can remain the same, though you might want to give slightly higher weighting for events in overtime.
- **Edge Cases:** Consider blowout scenarios (large lead). If the game is not close, fewer “exciting” events may appear. The algorithm should still produce 10 highlights if possible, but they may have relatively lower impact scores.

---

## 6. Acceptance Criteria

- **Reproducibility:** Given the same set of play-by-play data, the algorithm should consistently produce the same top 10 highlights.
- **Relevance:** The top 10 events must be the most game-altering, exciting, or significant by the chosen weighting criteria.
- **Clarity:** Each highlight must have the required fields: time, period, score, and a short explanation.
