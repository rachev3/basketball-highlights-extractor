## Overall Structure

- The shot chart content is wrapped in a container with the class `shot-chart-wrap`.

---

## Team Titles

- **Team Titles Section**  
  Located at the top of the shot chart area:
  ```html
  <div class="shot-chart-title row">
    <div class="team-title-0 col col-6">
      <div class="bs-image">
        <span class="id_aj_1_logoT">
          <img src="..." />
        </span>
      </div>
      <span class="id_aj_1_name">Етрос</span>
    </div>
    <div class="team-title-1 col col-6">
      <div class="bs-image">
        <span class="id_aj_2_logoT">
          <img src="..." />
        </span>
      </div>
      <span class="id_aj_2_name">Дрийм тийм Троян</span>
    </div>
  </div>
  ```
  - **Team Logos** are inside `<span>` elements with classes `id_aj_1_logoT` (Team 0) and `id_aj_2_logoT` (Team 1).
  - **Team Names** are in `<span>` elements with IDs `aj_1_name` and `aj_2_name`.

---

## Shot Chart Controls

- **Control Panel Section**  
  Found within `<div class="shot-chart-control">`:

  - **Team Filter:**

    ```html
    <h4 class="filter-name">Team:</h4>
    <a
      href="#"
      class="team1"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_tn1',1);return false;"
    >
      <span class="id_aj_1_shortName">Етрос</span>
    </a>
    <a
      href="#"
      class="control"
      id="sc_tn2"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_tn2',1);return false;"
    >
      <span class="id_aj_2_shortName">Дрийм тийм Троя...</span>
    </a>
    <a
      href="#"
      data-link="both"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_img',1);return false;"
      class="all-shots active-filter"
      >Both</a
    >
    ```

    - Clicking these links filters the shot markers by team.

  - **Period Filter:**
    ```html
    <h4 class="filter-name">Period:</h4>
    <a
      class="sc_link1"
      href="#"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_per1',1);return false;"
      >1</a
    >
    <a
      class="sc_link2"
      href="#"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_per2',1);return false;"
      >2</a
    >
    <a
      class="sc_link3"
      href="#"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_per3',1);return false;"
      >3</a
    >
    <a
      class="sc_link4"
      href="#"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_per4',1);return false;"
      >4</a
    >
    <h4 class="inOvertime" style="display: none;">
      <a
        href="#"
        onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_perot',1);return false;"
        class="all-shots"
        >OT</a
      >
    </h4>
    <a
      href="#"
      data-link="all"
      onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_img','span',1);return false;"
      class="all-shots active-filter"
      >All</a
    >
    ```
    - These links allow filtering shots by period (1, 2, 3, 4, OT, or All).
    - The active filter is indicated by the class `active-filter`.

---

## Player Shot Chart Tables

- **Player Tables** are displayed on the left side.
- There are separate tables for each team:

  - **Team 0 (e.g., "Етрос") Table:**
    ```html
    <table class="team1sc">
      <thead>
        <tr class="legend-row">
          <th class="sc-p-no">No.</th>
          <th class="sc-p-name">Player</th>
          <th class="sc-points">Pts</th>
        </tr>
      </thead>
      <tbody class="team-0-person-container">
        <tr class="player-row row-not-used" id="aj_1_0_row">
          <td class="sc-p-no"><span id="aj_1_0_shirtNumber"></span></td>
          <td class="sc-p-name">
            <a
              href="#"
              onclick="toggleclasses('shotchart2536064','shotchart','sc_img','sc_pn0 sc_tn1',1);return false;"
            >
              <span id="aj_1_0_name"></span>
            </a>
          </td>
          <td class="sc-points"><span id="aj_1_0_sPoints"></span></td>
        </tr>
        <!-- More player rows here -->
      </tbody>
    </table>
    ```
  - **Team 1 (e.g., "Дрийм тийм Троян") Table:**  
    Similar structure with table class `team2sc` and IDs starting with `aj_2_`.

- **Player Row Details:**
  - **Player Number:** Found in a `<span>` (e.g., `aj_1_5_shirtNumber`).
  - **Player Name:** In a `<span>` (e.g., `aj_1_5_name`) inside an anchor link.
  - **Points:** Displayed in `<span>` with an ID like `aj_1_5_sPoints`.

---

## Shot Chart Data Visualization

- **Shot Chart Container:**  
  The actual shot markers are rendered within:

  ```html
  <div id="shotchartholder" class="col col-8">
    <div id="shotchart">
      <div id="shotchart_data">
        <!-- Shot markers as span elements -->
      </div>
    </div>
  </div>
  ```

- **Shot Marker Elements:**  
  Each shot is represented by a `<span>` with:
  - **Classes:**
    - `sc_img` – base class for shot markers.
    - Outcome classes such as `white_made`, `white_missed`, `black_made`, or `black_missed`.
    - Period classes (e.g., `sc_per1`, `sc_per2`, etc.).
    - Player indicator class (e.g., `sc_pn2` means player number 2).
    - Team indicator class (`sc_tn1` for Team 0; `sc_tn2` for Team 1).
  - **Inline Style:**  
    The `bottom` and `left` CSS properties (expressed in percentages) position the marker on the chart.
  - **Title Attribute:**  
    Contains a text description, for example:
    ```html
    title="6, Дзен Дай, 2pt lay up"
    ```
    which includes the player’s number, name, and shot type.

---

## Scoring Breakdown Graphs

- **Location:**  
  Found in the section below the shot chart inside `<div class="lower-sc-wrap row">`.

- **Graph Elements:**  
  For each team, there are several graph wrappers that summarize shooting percentages:

  - **Structure Example (Team 0 - 2P):**
    ```html
    <div class="graph-wrapper team-0 reverseChart">
      <div class="csspie big" data-start="50" data-value="29"></div>
      <div class="csspie" data-start="79" data-value="71"></div>
      <div class="chartLabel">2P</div>
      <div class="pie-overlay">
        <span class="chartValue id_aj_1_tot_sTwoPointersPercentage">29</span>%
      </div>
      <div class="chartSummary">
        <span class="id_aj_1_tot_sTwoPointersMade">11</span>/<span
          class="id_aj_1_tot_sTwoPointersAttempted"
          >37</span
        >
      </div>
    </div>
    ```
  - **Graph Components:**
    - **CSS Pie Elements:**  
      Use the `csspie` class with `data-start` and `data-value` attributes to render percentage arcs.
    - **Label:**  
      A `<div class="chartLabel">` displays the shot type (e.g., "2P", "3P", "FT").
    - **Percentage Overlay:**  
      `<div class="pie-overlay">` shows the shot percentage (e.g., `29%`).
    - **Summary:**  
      `<div class="chartSummary">` shows made/attempted counts.

- **Separate graphs are available for:**
  - 2-Point Field Goals (2P)
  - 3-Point Field Goals (3P)
  - Free Throws (FT)  
    (For each team.)

---

## Interactive Elements and Filtering

- **User Interaction:**
  - The shot chart controls use anchor links with `onclick` events that call the JavaScript function `toggleclasses`.
  - This function is used to filter the shot markers based on team, period, or individual player.
- **Active Filter Indication:**

  - The currently selected filter is marked by adding the class `active-filter` to the link.

- **Additional JS:**
  - JavaScript snippets update the active filter state when users click on a team or period link.
  - There is a lexicon object (similar to the one in the play-by-play documentation) that maps shorthand event codes to descriptive text.

---

## Hidden Aggregated Data

- **Hidden Totals:**  
  A hidden `<div style="display:none">` contains `<span>` elements with overall shot totals, such as:
  ```html
  <span id="aj_1_tot_sFieldGoalsMade">19</span>
  <span id="aj_1_tot_sFieldGoalsAttempted">69</span>
  <span id="aj_1_tot_sFieldGoalsPercentage">27</span>
  ...
  ```
  These can be used to drive the scoring breakdown graphs or for further analysis.

---

## Summary

- **Team and Player Information:**  
  Extract team logos and names from the title section and player details from the left-side tables.
- **Shot Chart Visualization:**  
  Each shot is an individual `<span>` element in the `shotchart_data` container. Its classes and inline styles provide:

  - Outcome (made/missed)
  - Period information
  - Position (via `bottom` and `left`)
  - Associated player and team (via classes like `sc_pnX` and `sc_tnY`)
  - Descriptive text in the `title` attribute

- **Scoring Breakdown:**  
  The lower section contains pie chart graphs summarizing shooting performance (2P, 3P, FT) for each team.

- **Interactivity:**  
  Filtering is managed via JavaScript functions that toggle classes to show/hide shot markers based on the selected criteria.
