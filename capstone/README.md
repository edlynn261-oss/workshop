# 🚕 NYC Yellow Taxi Data Analysis | Capstone Project

**Analysis period:** January–March 2024  
**Repository:** [edlynn261-oss/workshop](https://github.com/edlynn261-oss/workshop)  
**Project folder:** `capstone/`

## Project Overview

This capstone explores New York City Yellow Taxi trip records to understand demand, revenue, pickup locations, travel times, payment methods, and airport travel. The workflow uses **DuckDB** to store and query data, **dbt** to clean and transform records, **Python** for analysis, and **Streamlit with Plotly** for interactive visualizations.

The analysis uses **cleaned trips**, not every record in the raw source files.

## Business Questions

1. How many taxi trips occurred, and how much revenue was generated, each month?
2. Which ten pickup zones are busiest, and which borough earns the most revenue?
3. What are the busiest pickup hours and days of the week?
4. How does recorded tipping differ across payment types?
5. How important are trips to or from JFK, LaGuardia, and Newark airports?

## Tools and Technologies

| Tool | Purpose |
| --- | --- |
| Python | Analysis and scripting |
| DuckDB | Analytical database and SQL execution |
| dbt | Staging, transformation, and reporting models |
| Pandas | Data processing and tabular output |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts |
| GitHub Codespaces | Development environment |

## Data Preparation and Quality Rules

The dbt staging model `taxi_dbt/models/staging/stg_trips.sql` reads from the raw taxi trip source and applies these rules:

- Pickup timestamps from **2024-01-01** through **2024-03-31** (before 2024-04-01).
- Trip distance greater than 0 and less than 100 miles.
- Positive fare amount and total amount.
- Trip duration between 1 and 180 minutes.

The staging model retains pickup/drop-off timestamps and zone IDs, passenger count, distance, payment type, fare, tip, total amount, and duration.

The zone lookup model provides zone names, boroughs, and service-zone labels.

## Data Model

The implemented dbt workflow uses cleaned staging models and aggregated reporting models. A star schema with a central trip fact table and zone, datetime, and payment dimensions can also be used as a conceptual design, but should not be confused with tables already materialized in this repository.

**Grain:** One cleaned row represents one taxi trip.

## Analysis Results

### Q1 — Monthly Trips and Revenue

| Month | Trips | Revenue (USD) | Average Distance (miles) |
| --- | ---: | ---: | ---: |
| January 2024 | 2,858,964 | $78,055,362.00 | 3.30 |
| February 2024 | 2,891,151 | $78,640,842.87 | 3.23 |
| March 2024 | 3,427,498 | $95,367,987.28 | 3.37 |

March recorded the highest monthly trip volume and revenue. From January to March, trips rose by approximately **19.9%** and revenue by approximately **22.2%**.

### Q2 — Pickup Zones and Borough Revenue

- **Midtown Center** had the most pickups: **441,006 trips**.
- **JFK Airport** generated approximately **$33.21 million** among the ten busiest pickup zones, despite ranking fourth by trip count.
- **Manhattan** generated the highest pickup-borough revenue: approximately **$190.71 million**, from **8.26 million trips**.

### Q3 — Peak Hours and Days

- The busiest pickup hour was **6:00 PM**, with **664,953 trips**.
- The quietest hour was **4:00 AM**, with **52,375 trips**.
- **Thursday** recorded the highest aggregate weekday trip count (**1,486,625 trips**) during the analysis period.

Weekday totals are aggregated across the quarter; they are not normalized by the number of occurrences of each weekday.

### Q4 — Tipping by Payment Type

Credit card trips recorded approximately **$30.09 million in tips**, averaging **$4.19 per trip**. About **95.12%** of credit card trips had a positive recorded tip amount.

**Interpretation caution:** The taxi dataset generally captures electronically recorded tips; cash tips are not reliably represented. Low recorded cash tips should not be interpreted as proof that cash-paying passengers do not tip.

### Q5 — Airport vs. Non-Airport Trips

Airport trips are defined as trips with either pickup or drop-off zone corresponding to **JFK (132), LaGuardia (138), or Newark (1)**.

| Metric | Airport | Non-Airport |
| --- | ---: | ---: |
| Trips | 869,548 | 8,308,065 |
| Share of trips | 9.47% | 90.53% |
| Total revenue | $67,620,937.94 | $184,443,254.21 |
| Share of revenue | 26.83% | 73.17% |
| Average fare | $56.14 | $14.75 |
| Average duration | 36.03 min | 13.41 min |

Airport trips accounted for **9.47% of trips but 26.83% of revenue**, making them an economically important segment.

## Project Structure

The following structure shows the principal files and the intended locations of the five analysis models. **The Q2–Q5 model files may need to be committed from Codespaces before they appear on GitHub.**

```text
capstone/
├── README.md
├── dashboard.py
├── requirements.txt
├── warehouse/
│   └── taxi.duckdb             # local database, if generated
└── taxi_dbt/
    ├── dbt_project.yml
    ├── profiles.yml
    └── models/
        ├── staging/
        │   ├── stg_trips.sql
        │   └── stg_zones.sql
        └── marts/
            ├── trips_by_month.sql
            ├── pickup_zone_analysis.sql     # Q2; commit if local
            ├── pickup_time_analysis.sql     # Q3; commit if local
            ├── payment_tipping_analysis.sql # Q4; commit if local
            └── airport_trip_analysis.sql    # Q5; commit if local
```

## Running the Project in GitHub Codespaces

### 1. Open the capstone folder

```bash
cd ~/workshop/capstone
```

### 2. Install dashboard dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure that **dbt with the DuckDB adapter** is also installed for model builds:

```bash
python -m pip install dbt-duckdb
```

### 3. Build dbt models

Make sure the raw DuckDB tables and taxi-zone lookup data have already been loaded according to the workshop setup.

```bash
cd ~/workshop/capstone/taxi_dbt
dbt run
dbt test
```

The dbt profile points to `../warehouse/taxi.duckdb`, relative to the `taxi_dbt` directory.

### 4. Start the Streamlit dashboard

```bash
cd ~/workshop/capstone
python -m streamlit run dashboard.py
```

Open the forwarded **port 8501** in GitHub Codespaces.

The dashboard reads reporting tables from `capstone/warehouse/taxi.duckdb`. It expects these models to exist:

- `trips_by_month`
- `pickup_zone_analysis`
- `pickup_time_analysis`
- `payment_tipping_analysis`
- `airport_trip_analysis`

**Note:** The dashboard queries the DuckDB tables directly, rather than reading text printed in the terminal by the individual Python analysis scripts. Its current charts show pre-aggregated results and do not apply a dynamic month filter to all analyses.

## Overall Conclusion

The results show increasing taxi demand through the first quarter of 2024, strong pickup activity in Manhattan, pronounced evening demand, high electronically recorded tipping on credit card trips, and an outsized revenue contribution from airport travel. These findings can support fleet planning, staffing, demand analysis, and revenue management.

## Data Source and Limitations

Source: [NYC Taxi & Limousine Commission (TLC) Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

The results reflect the project's cleaning filters and the first three months of 2024, not all NYC taxi journeys or a full year. Revenue is calculated as the sum of the recorded `total_amount` field for included trips. Airport classification uses taxi-zone IDs and includes trips starting **or** ending at an airport.

---

*Prepared for the NYC Yellow Taxi data analytics capstone.*
