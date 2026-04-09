# NYC Shootings Dashboard

## Overview
This project analyzes New York City shooting incident data to uncover patterns in **where**, **when**, and **under what conditions** shootings occur.

The goal is to move beyond raw counts and identify meaningful patterns through proper normalization and interactive visualization.

---

## Key Insights

- **Geographic Concentration:** Shootings are disproportionately concentrated in the Bronx when adjusted for population.
- **Time of Day:** Incidents peak during nighttime hours, especially between 8 PM and midnight.
- **Day Type:**  
  **Shootings occur more frequently on weekends when adjusted for the number of days.**

Together, these findings suggest that shootings are not random, but instead cluster in specific high-risk windows—particularly **weekend nights**.

---

## Interactive Dashboard

👉 *(Add your Streamlit link here once deployed)*

The dashboard allows users to:
- Filter by borough and time of day
- Explore shooting patterns across multiple dimensions
- Compare normalized vs raw metrics

---

## Methodology

### Data Preparation
- Cleaned and standardized borough and demographic fields
- Parsed dates and extracted:
  - Hour of occurrence
  - Day of week
  - Time-of-day groupings

### Feature Engineering
- Created:
  - `day_type` (weekday vs weekend)
  - `time_of_day` (morning, afternoon, evening, night)

### Normalization Strategy
To ensure fair comparisons:
- **Per capita** for borough comparisons
- **Per day** for weekday vs weekend comparisons
- **Per hour** for time-of-day analysis

This step was critical—without normalization, conclusions would be misleading.

---

## Tech Stack

- Python (pandas, numpy)
- Altair (data visualization)
- Streamlit (interactive dashboard)
- Jupyter Notebook (analysis and documentation)

---

## Repository Structure
```text
├── app.py                  # Streamlit app  
├── data/                   # Cleaned dataset  
├── src/                    # Data + chart logic  
├── notebooks/              # Full analysis notebook  
└── README.md
```

---

## Limitations

- Does not account for population movement (e.g., nightlife patterns)
- External factors (weather, holidays, events) are not included
- Time-of-day grouping simplifies more granular variation

Future work could incorporate these variables to refine the analysis.

---

## Author

John Creath  
Master’s in Data Science — University of Colorado Boulder

---

## Why This Project Matters

Understanding when and where shootings occur can support more targeted prevention strategies.

This project demonstrates not just technical execution, but the importance of **correct analytical framing and normalization** in drawing meaningful conclusions from data.
