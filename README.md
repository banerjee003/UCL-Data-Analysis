# UEFA Champions League Data Analysis

## Overview

This project analyzes UEFA Champions League match data from the last decade to uncover patterns in team performance, goal trends, and the impact of home advantage. The analysis was performed using Python with Pandas for data manipulation and Seaborn/Matplotlib for visualization.

## Objectives

* Analyze total matches and goals scored by each team
* Calculate win percentages combining home and away performance
* Study home advantage across seasons
* Identify high-scoring teams and matches
* Explore goal trends over different UCL seasons

## Dataset

The dataset contains match-level information with the following key fields:

* home_team, away_team
* home_goals, away_goals
* result (H/A/D)
* season

A simplified version of the dataset was created to focus on core analysis.

## Tools & Libraries

* Python
* Pandas – data cleaning and aggregation
* NumPy – numerical operations
* Seaborn & Matplotlib – visualization
* Jupyter Notebook

## Analysis Performed

### 1. Match Outcome Analysis

* Distribution of home wins, away wins, and draws
* Calculation of home advantage percentage
* Season-wise home win trends

### 2. Team Performance

* Total matches played by each team
* Total goals scored (home + away)
* Most successful teams by win percentage
* Teams with most high-scoring matches (5+ goals)

### 3. Goal Trends

* Goals scored per season
* Identification of highest scoring season
* Comparison of home vs away goal contribution

## Key Insights

* Home teams win a significant proportion of matches, confirming the presence of home advantage in the Champions League.
* A small group of elite clubs dominate in terms of total goals and win percentage.
* Goal scoring peaked in specific seasons, indicating tactical shifts toward more attacking football.
* High-scoring matches (5+ goals) are concentrated among top European teams.
* Teams with strong home records generally show better overall tournament performance.

## Visualizations Included

* Top teams by total matches played
* Top goal scoring teams
* Goals per season trend
* Home win percentage by season
* Team win percentage ranking

## How to Run

1. Clone the repository
2. Install required libraries
3. Open the Jupyter Notebook
4. Run all cells sequentially

```bash
pip install pandas numpy matplotlib seaborn
```

## Project Structure

* ucl_super_easy.csv – simplified dataset
* UCL_Analysis.ipynb – main analysis notebook
* README.md – project documentation

## Future Scope

* Add player-level analysis
* Compare knockout vs group stage performance
* Include expected goals (xG) metrics
* Build an interactive dashboard

## Author

Pallab Banerjee
