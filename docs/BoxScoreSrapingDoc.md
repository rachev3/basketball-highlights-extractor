## Overall Team Information

- **Team Names**

  - First team:
    ```html
    <span id="aj_1_name">{name of the first team}</span>
    ```
  - Second team:
    ```html
    <span id="aj_2_name">{name of the second team}</span>
    ```

- **Box Score Containers**

  - First team’s box score:
    ```html
    <div class="boxscorewrap team-0-bs"></div>
    ```
  - Second team’s box score:
    ```html
    <div class="boxscorewrap team-1-bs"></div>
    ```

- **Match Staff (Optional)**

  - On desktop:
    ```html
    <div class="match-staff desktop-only"></div>
    ```
    (Shows Coach and Assistant info)
  - On mobile:
    ```html
    <div class="match-staff mobile-only"></div>
    ```

- **Team Statistics**
  - First team stats:
    ```html
    <div class="team-stats team-0-ts"></div>
    ```
  - Second team stats:
    ```html
    <div class="team-stats team-1-ts"></div>
    ```
  - Example statistics include: Points from turnovers, Points in the paint, Second chance points, Fast break points, Bench points, Biggest Lead, and Biggest Scoring Run.

---

## Player Row Structure

Within each box score table, player data is organized in `<tr>` elements.

- **Player Rows:**

  - Each player is represented by a `<tr>` element with a class starting with `"player-row"`.
  - **Ignore:** There is one `<tr class="player-row row-not-used">` per team which does not contain valid player data.

- **Starter vs. Bench:**
  - Starter players typically include an additional class like `p_starter`.
  - Bench players include a class like `p_notstarter`.

---

## Extraction Details from Each Player’s `<tr>`

For each player row (excluding the row-not-used):

1. **Player Number**

   - **HTML:**
     ```html
     <td class="center num playernum">
       <span id="aj_1_6_shirtNumber" class="aj_9">{player's number}</span>
     </td>
     ```
   - **Extraction:**
     - Get the text inside the `<span>` (e.g., `"9"`).

2. **Player Name**

   - **HTML:**
     ```html
     <td class="left playerinfo" oid="">
       <a href="#" id="pop-action_1_6" class="playerpopup" tno="1" pno="6">
         <span id="aj_1_6_name" class="aj_Д. Мангов">{player's name}</span>
       </a>
       <span id="aj_1_6_captainString"></span>
     </td>
     ```
   - **Extraction:**
     - Get the text inside the `<span>` with the ID ending in `_name` (e.g., `"Димитър Мангов"`).
     - The adjacent `<span id="..._captainString">` can indicate captaincy if it contains a value.

3. **Player Position**

   - **HTML:**
     ```html
     <td class="center tablet">
       <span id="aj_1_6_playingPosition" class="aj_PF"> {position}</span>
     </td>
     ```
   - **Extraction:**
     - Get the text inside the `<span>` (e.g., `"PF"`).

4. **Minutes Played**

   - **HTML:**
     ```html
     <td class="center mobile-p">
       <span id="aj_1_6_sMinutes" class="aj_18:13">{time}</span>
     </td>
     ```
   - **Extraction:**
     - Get the text (e.g., `"18:13"` representing 18 minutes and 13 seconds).

5. **Points Scored**

   - **HTML:**
     ```html
     <td class="center">
       <span id="aj_1_6_sPoints" class="aj_4">{points}</span>
     </td>
     ```
   - **Extraction:**
     - Get the text inside the `<span>` (e.g., `"4"`).

6. **Field Goals (FG) Made and Attempted**

   - **HTML:**
     ```html
     <td class="center">
       <span id="aj_1_6_sFieldGoalsMade" class="aj_2">2</span>-
       <span id="aj_1_6_sFieldGoalsAttempted" class="aj_4">4</span>
     </td>
     ```
   - **Extraction:**
     - **Made:** Text from the first `<span>` (e.g., `"2"`).
     - **Attempted:** Text from the second `<span>` (e.g., `"4"`).

7. **Field Goals Percentage (FG%)**

   - **HTML:**
     ```html
     <td class="center mobile-l percent">
       <span id="aj_1_6_sFieldGoalsPercentage" class="aj_50">{percentage}</span>
     </td>
     ```
   - **Extraction:**
     - Get the percentage value (e.g., `"50"`).

8. **2-Point Field Goals Made and Attempted**

   - **HTML:**
     ```html
     <td class="center mobile-p">
       <span id="aj_1_6_sTwoPointersMade" class="aj_2">2</span>-
       <span id="aj_1_6_sTwoPointersAttempted" class="aj_4">4</span>
     </td>
     ```
   - **Extraction:**
     - **Made:** Text from the first `<span>` (e.g., `"2"`).
     - **Attempted:** Text from the second `<span>` (e.g., `"4"`).

9. **2-Point Field Goals Percentage (2P%)**

   - **HTML:**
     ```html
     <td class="center mobile-l percent">
       <span id="aj_1_6_sTwoPointersPercentage" class="aj_50"
         >{percentage}</span
       >
     </td>
     ```
   - **Extraction:**
     - Get the percentage value (e.g., `"50"`).

10. **3-Point Field Goals Made and Attempted**

    - **HTML:**
      ```html
      <td class="center mobile-p">
        <span id="aj_1_6_sThreePointersMade" class="aj_0">0</span>-
        <span id="aj_1_6_sThreePointersAttempted" class="aj_0">0</span>
      </td>
      ```
    - **Extraction:**
      - **Made:** Text from the first `<span>` (e.g., `"0"`).
      - **Attempted:** Text from the second `<span>` (e.g., `"0"`).

11. **3-Point Field Goals Percentage (3P%)**

    - **HTML:**
      ```html
      <td class="center mobile-l percent">
        <span id="aj_1_6_sThreePointersPercentage" class="aj_0"
          >{percentage}</span
        >
      </td>
      ```
    - **Extraction:**
      - Get the percentage value (e.g., `"0"`).

12. **Free Throws Made and Attempted**

    - **HTML:**
      ```html
      <td class="center mobile-p">
        <span id="aj_1_6_sFreeThrowsMade" class="aj_0">0</span>-
        <span id="aj_1_6_sFreeThrowsAttempted" class="aj_0">0</span>
      </td>
      ```
    - **Extraction:**
      - **Made:** Text from the first `<span>` (e.g., `"0"`).
      - **Attempted:** Text from the second `<span>` (e.g., `"0"`).

13. **Free Throws Percentage (FT%)**

    - **HTML:**
      ```html
      <td class="center mobile-l percent">
        <span id="aj_1_6_sFreeThrowsPercentage" class="aj_0">{percentage}</span>
      </td>
      ```
    - **Extraction:**
      - Get the percentage value (e.g., `"0"`).

14. **Rebounds**

    - **Offensive Rebounds:**
      ```html
      <td class="center tablet">
        <span id="aj_1_6_sReboundsOffensive" class="aj_3"
          >{offensive rebounds}</span
        >
      </td>
      ```
    - **Defensive Rebounds:**
      ```html
      <td class="center tablet">
        <span id="aj_1_6_sReboundsDefensive" class="aj_4"
          >{defensive rebounds}</span
        >
      </td>
      ```
    - **Total Rebounds:**
      ```html
      <td class="center">
        <span id="aj_1_6_sReboundsTotal" class="aj_7">{total rebounds}</span>
      </td>
      ```
    - **Extraction:**
      - Extract each corresponding value from the respective `<span>` elements.

15. **Assists**

    - **HTML:**
      ```html
      <td class="center">
        <span id="aj_1_6_sAssists" class="aj_1">{assists}</span>
      </td>
      ```
    - **Extraction:**
      - Get the number of assists (e.g., `"1"`).

16. **Turnovers**

    - **HTML:**
      ```html
      <td class="center mobile-p">
        <span id="aj_1_6_sTurnovers" class="aj_0">{turnovers}</span>
      </td>
      ```
    - **Extraction:**
      - Get the number of turnovers (e.g., `"0"`).

17. **Steals**

    - **HTML:**
      ```html
      <td class="center">
        <span id="aj_1_6_sSteals" class="aj_0">{steals}</span>
      </td>
      ```
    - **Extraction:**
      - Get the steals (e.g., `"0"`).

18. **Blocks**

    - **HTML:**
      ```html
      <td class="center">
        <span id="aj_1_6_sBlocks" class="aj_0">{blocks}</span>
      </td>
      ```
    - **Extraction:**
      - Get the blocks (e.g., `"0"`).

19. **Blocks Received**

    - **HTML:**
      ```html
      <td class="center tablet">
        <span id="aj_1_6_sBlocksReceived" class="aj_0">{blocks received}</span>
      </td>
      ```
    - **Extraction:**
      - Get the value (e.g., `"0"`).

20. **Personal Fouls**

    - **HTML:**
      ```html
      <td class="center mobile-p">
        <span id="aj_1_6_sFoulsPersonal" class="aj_1">{personal fouls}</span>
      </td>
      ```
    - **Extraction:**
      - Get the number of fouls (e.g., `"1"`).

21. **Fouls On**

    - **HTML:**
      ```html
      <td class="center tablet">
        <span id="aj_1_6_sFoulsOn" class="aj_0">{fouls on}</span>
      </td>
      ```
    - **Extraction:**
      - Get the value (e.g., `"0"`).

22. **Plus/Minus**

    - **HTML:**
      ```html
      <td class="center">
        <span id="aj_1_6_sPlusMinusPoints" class="aj_10">{plus/minus}</span>
      </td>
      ```
    - **Extraction:**
      - Get the plus/minus figure (e.g., `"10"`).

23. **Efficiency Index (Index)**
    - **HTML:**
      ```html
      <td class="center bs_eff tablet">
        <span id="aj_1_6_eff_5" class="aj_9">{efficiency index}</span>
      </td>
      ```
    - **Extraction:**
      - Get the efficiency number (e.g., `"9"`).

---

## Notes on the ID Patterns

- **ID Naming Convention:**

  - Each statistic field uses a consistent naming pattern where the IDs include:
    - A prefix indicating the team (`aj_1_` for the first team, `aj_2_` for the second team).
    - A number representing the player’s index in the table.
    - A suffix indicating the type of statistic (e.g., `_sMinutes` for minutes, `_sPoints` for points, `_sFieldGoalsMade` for field goals made, etc.).

- **Team and Player Association:**
  - The player’s row ID and the IDs within that row include numbers (e.g., `aj_1_6_`) that link all statistics for that specific player.
