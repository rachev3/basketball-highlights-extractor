## Overall Structure

- The play-by-play section is contained within a `<div class="play-by-play">` element.

## Play-by-Play Events

- The events are contained within the nested elements:
  ```html
  <div class="pbpwrap">
    <div class="pbpscroll">
      <div id="playbyplay">
        <div id="aj_pbp">
          <!-- Play-by-play events here -->
        </div>
      </div>
    </div>
  </div>
  ```

### Structure of a Single Play-by-Play Event

Each event is represented by a `<div>` element with a set of classes and child elements:

1. **Event Container**

   - **Example:**
     ```html
     <div
       id="00:05"
       class="pbpa pbpt2 pbptyfreethrow per_4 per_reg 2of2 freethrow"
     >
       <!-- Event details -->
     </div>
     ```
   - **ID:**
     - Typically a time stamp (e.g., `"00:05"`).
   - **Classes:**
     - `pbpa` – indicates a play-by-play action.
     - `pbptX` – a numeric type indicator (e.g., `pbpt0`, `pbpt1`, `pbpt2`).
     - `pbptyEVENT` – indicates the event type (e.g., `pbptyfreethrow`, `pbptyfoulon`, `pbptyrebound`, `pbptyassist`, `pbptyturnover`, etc.).
     - `per_#` – indicates the period (e.g., `per_4` for period 4).
     - `per_reg` – indicates a regular period (alternatively, you might see other modifiers for overtime).
     - Additional modifiers may appear (e.g., `2of2`, `1of2`, `end`, `start`).

2. **Team Container**

   - **Element:**
     ```html
     <div class="pbp-team pbp-team2 [optional: scaction]">
       <!-- Team-specific details -->
     </div>
     ```
   - **Class Explanation:**
     - `pbp-team1` or `pbp-team2` indicates the team involved in the event.
     - An additional class like `scaction` may appear for scoring actions.

3. **Time and Score Information**

   - **Element:**
     ```html
     <div class="pbp-time">
       <span class="pbp-period">P4</span> 00:05<span class="pbpsc">50-57</span>
     </div>
     ```
   - **Extraction:**
     - **Period:** The `<span class="pbp-period">` element shows the period (e.g., `"P4"`).
     - **Timestamp:** The text following the period span (e.g., `"00:05"`) indicates the time of the event.
     - **Score:** The `<span class="pbpsc">` element shows the current score after the event (e.g., `"50-57"`).

4. **Action Description**

   - **Element:**
     ```html
     <div class="pbp-action">
       <strong>3, Илия Маринов</strong>, Free throw 2 of 2 made <br />
       <span class="pbp-team-name">Дрийм тийм Троян</span> - lead by 7
     </div>
     ```
   - **Extraction:**
     - **Player Information:**
       - The `<strong>` element usually contains the player's number and name (e.g., `"3, Илия Маринов"`).
     - **Action Details:**
       - The text following the `<strong>` tag describes the action (e.g., `"Free throw 2 of 2 made"`).
     - **Team Name (Optional):**
       - A `<span class="pbp-team-name">` element may be present to reiterate the team (e.g., `"Дрийм тийм Троян"`).
     - **Additional Context:**
       - Extra text (e.g., `" - lead by 7"`) may indicate the change in the score margin.

5. **Visual Elements**
   - **Images:**
     - `<img class="pbp-logo" src="...">` shows the team logo.
     - `<img class="pbp-player-photo" src="...">` shows a player’s photo (if available).
   - **Team Color Box:**
     - `<span class="teamcolorbox team1color"></span>` or `<span class="teamcolorbox team2color"></span>` is used to visually represent the team color.

---

## Examples of Specific Event Types

- **Game and Period Events:**

  - **Game End:**
    ```html
    <div id="00:00" class="pbpa pbpt0 pbptygame per_4 per_reg end game">
      <div class="description">Game end</div>
      <span class="pbpsc">50-57</span>
    </div>
    ```
  - **Period End:**
    ```html
    <div id="00:00" class="pbpa pbpt0 pbptyperiod per_4 per_reg end period">
      <div class="description">Period end</div>
      <span class="pbpsc">50-57</span>
    </div>
    ```

- **Free Throw Events:**

  - The event container will include `pbptyfreethrow` and modifiers such as `1of2` or `2of2`. The action text specifies the free throw attempt and result.

- **Foul Events:**

  - Events related to fouls use classes like `pbptyfoulon` or `pbptyfoul` and contain descriptions such as “Personal foul” or “Foul on”.

- **Rebound Events:**

  - Identified by the class `pbptyrebound` along with additional descriptive text (e.g., “Defensive rebound” or “Offensive rebound”).

- **Shot Events (2pt, 3pt, Layup, etc.):**

  - Use classes such as `pbpty3pt` for three-point attempts or `pbpty2pt` for two-point attempts.
  - Additional shot type modifiers like `jumpshot`, `layup`, `drivinglayup`, `tipinlayup`, etc. are included.
  - The action description details whether the shot was made or missed.

- **Other Events:**
  - **Assist:**  
    Uses class `pbptyassist`. The action description will state “Assist.”
  - **Turnover:**  
    Uses class `pbptyturnover` with modifiers such as `badpass`, `ballhandling`, etc.
  - **Steal:**  
    Uses class `pbptysteal` and the action description states “Steal.”
  - **Block:**  
    Uses class `pbptyblock` and indicates a “Block.”
  - **Substitution:**  
    Uses class `pbptysubstitution` with further class modifiers like `in substitution` or `out substitution`. The action description specifies the substitution (e.g., “Substitution in” or “Substitution out”).
  - **Timeout:**  
    Uses class `pbptytimeout` with modifiers such as `full timeout` (e.g., “Timeout - full”).

---

## Additional Information

- **Lexicon Mapping:**  
  A JavaScript lexicon object is included in the page that maps short event codes (e.g., `"freethrow.1of2"`) to full descriptive text (e.g., `"Free throw 1 of 2"`). This can be used to standardize or interpret the event descriptions.

- **Hidden Metadata:**  
  Hidden input elements (e.g., `<input type="hidden" id="matchId" value="2536064">`) provide additional metadata about the match but are not part of the play-by-play event extraction.
