# Assignment: Play‑by‑Play Scraper

## 1. Objective

Build a scraper that fetches **all** play‑by‑play events from a given game page (all quarters), and outputs them as a structured data file (JSON or CSV). We are **not** yet doing any analysis or highlight extraction—just a faithful scrape of every event.

url: https://comps.basketball.bg/game_play.inc.php?g_id={id}

id is the game id

Example for real game: https://comps.basketball.bg/game_play.inc.php?g_id=374043

## 2. Target Page Structure

On each game page, the play‑by‑play lives inside a series of `<table class="tbl_play" id="q_[1–4|OT]">` blocks.  
Each row (`<tr>`) represents either:

- a **non‑scoring event** (no score change)
- or a **scoring event** (class `tr_score`) with an updated `<div class="score"><span>home</span><span>away</span></div>`

Within each row:

- **Home column**: `<td class="td_info td_home">…</td>`
- **Timestamp**: `<td class="td_score"><div class="time">MM:SS</div></td>`
- **Away column**: `<td class="td_info td_away">…</td>`

Example event text:

```html
<div class="div_info">
  <a href="player-26485-maksim-naumov" class="player_name">Максим Наумов</a>
  наказателен удар 2от2<br />успешен (9 точки)
</div>
```

## 3. Requirements

1. **Language & Libraries**

   - Python 3.x
   - `requests` (or `httpx`) for HTTP
   - `BeautifulSoup` (or `lxml`) for HTML parsing

2. **Data Extraction**  
   For **each** event row, extract:

   - `quarter` (from the table’s `id="q_4"` → `Q4`; handle OT as `OT1`, `OT2`…)
   - `time` (string `"MM:SS"`)
   - `team` (`"home"` or `"away"` depending which side has content)
   - `player_name` (text of `<a class="player_name">…</a>`, if present)
   - `event_text` (inner HTML/text of `.div_info`, preserving line breaks)
   - `home_score` & `away_score` (integers; only for rows with class `tr_score`; otherwise `null`)

3. **Pagination / Tabs**

   - The site may lazy‑load each quarter. Ensure your scraper triggers whatever endpoint (or JavaScript) is needed to retrieve the HTML for q1–q4.

4. **Output Format**

   - Save a flat list of event objects to a **JSON** file named `pbp_<game_id>.json`, or a **CSV** with columns:
     ```
     quarter,time,team,player_name,event_text,home_score,away_score
     ```

5. **Error Handling & Robustness**
   - Detect and log missing fields (e.g., rows with no `.div_info`).
   - Retry on transient HTTP failures.
   - Fail gracefully if the table structure changes (print a warning).

## 4. Implementation Outline

1. **Fetch page HTML**:
   ```python
   resp = requests.get(game_url)
   soup = BeautifulSoup(resp.text, "lxml")
   ```
2. **For each quarter** (`for q in [1,2,3,4,…]:`)
   - Locate `<table id=f"q_{q}">`
   - If it’s hidden behind JS, inspect network calls and replicate them.
3. **Iterate rows**:
   ```python
   for tr in table.find_all("tr"):
       is_score = "tr_score" in tr.get("class", [])
       # parse time, left cell, right cell, score if any
   ```
4. **Normalize data** & append to list.

5. **Write output**:
   ```python
   with open(f"pbp_{game_id}.json","w",encoding="utf8") as f:
       json.dump(events, f, ensure_ascii=False, indent=2)
   ```

## 5. Deliverables

1. **`scraper.py`**

   - Contains all scraping logic, configurable via command‑line (e.g. `python scraper.py --url <game_url>`).

2. **`requirements.txt`**

   - Pin versions of Requests and BeautifulSoup (or equivalent).

3. **Sample Output**

   - A JSON (or CSV) file for one real game demonstrating the full list of events.

4. **README.md**
   - Setup instructions (`pip install -r requirements.txt`).
   - How to run the scraper.
   - Notes on quarter‑loading and any gotchas.

## 6. Evaluation Criteria

- **Completeness:** Captures every single play event in all quarters/OT.
- **Correctness:** Fields properly parsed and typed.
- **Robustness:** Handles missing or unexpected markup without crashing.
- **Clarity:** Code is modular, commented, and easy to extend for new sites or leagues.

---

That spec should give a clear, self‑contained assignment for scraping all play‑by‑play events. Let me know if you’d like to drill into any part in more detail!
