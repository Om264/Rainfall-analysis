"""
rainfall_analysis.py
====================
A water resources data analysis script that:
  1. Creates a sample CSV file with rainfall measurements
  2. Reads and processes the data using pandas
  3. Calculates total and average rainfall statistics
  4. Prints a formatted summary report

Author: Water Resources Student
Requirements: pip install pandas
"""

import csv
import os
from datetime import date
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Create a sample CSV file with rainfall data
#
# Each row represents a daily rainfall reading at a specific station.
# Columns:
#   date         – measurement date (YYYY-MM-DD)
#   rainfall_mm  – rainfall depth in millimetres
#   location     – name of the gauging station
# ─────────────────────────────────────────────────────────────────────────────

CSV_FILE = "rainfall_data.csv"

# Sample dataset covering three monitoring stations over the same period.
# In a real project you would replace this with actual field measurements
# or data downloaded from a national hydrological database.
sample_data = [
    # date          rainfall_mm   location
    ["2024-06-01",  12.4,         "Station_A"],
    ["2024-06-01",   8.7,         "Station_B"],
    ["2024-06-01",  15.0,         "Station_C"],
    ["2024-06-02",   0.0,         "Station_A"],
    ["2024-06-02",   2.1,         "Station_B"],
    ["2024-06-02",   0.0,         "Station_C"],
    ["2024-06-03",  33.6,         "Station_A"],
    ["2024-06-03",  28.9,         "Station_B"],
    ["2024-06-03",  41.2,         "Station_C"],
    ["2024-06-04",   5.5,         "Station_A"],
    ["2024-06-04",   6.0,         "Station_B"],
    ["2024-06-04",   4.8,         "Station_C"],
    ["2024-06-05",  18.3,         "Station_A"],
    ["2024-06-05",  22.7,         "Station_B"],
    ["2024-06-05",  19.5,         "Station_C"],
    ["2024-06-06",   0.0,         "Station_A"],
    ["2024-06-06",   0.0,         "Station_B"],
    ["2024-06-06",   0.0,         "Station_C"],
    ["2024-06-07",   7.2,         "Station_A"],
    ["2024-06-07",   9.4,         "Station_B"],
    ["2024-06-07",   6.1,         "Station_C"],
]

# Write the data to a CSV file using Python's built-in csv module
with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "rainfall_mm", "location"])   # header row
    writer.writerows(sample_data)

print(f"[✓] Sample CSV created: '{CSV_FILE}'  ({len(sample_data)} records)\n")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Read the CSV file using pandas
#
# pandas is the standard library for tabular data in Python.
# parse_dates converts the 'date' column from plain strings into
# proper datetime objects so we can do time-based operations later.
# ─────────────────────────────────────────────────────────────────────────────

df = pd.read_csv(CSV_FILE, parse_dates=["date"])

# Quick inspection – always good practice after loading new data
print("─" * 55)
print("  RAW DATA PREVIEW (first 5 rows)")
print("─" * 55)
print(df.head(5).to_string(index=False))
print(f"\nDataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Date range   : {df['date'].min().date()}  →  {df['date'].max().date()}")
print(f"Locations    : {', '.join(sorted(df['location'].unique()))}\n")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Calculate statistics
#
# 3a. Overall statistics across the entire dataset
# 3b. Per-location breakdown (useful for spatial analysis)
# 3c. Per-date totals (areal average – common in hydrology)
# ─────────────────────────────────────────────────────────────────────────────

# ── 3a. Overall statistics ───────────────────────────────────────────────────
total_rainfall   = df["rainfall_mm"].sum()
average_rainfall = df["rainfall_mm"].mean()
max_rainfall     = df["rainfall_mm"].max()
min_rainfall     = df["rainfall_mm"].min()
rainy_days       = df[df["rainfall_mm"] > 0]["date"].nunique()
dry_days         = df[df["rainfall_mm"] == 0]["date"].nunique()

# ── 3b. Per-location statistics ──────────────────────────────────────────────
# groupby splits the DataFrame into one group per station,
# then we apply multiple aggregation functions in one call.
location_stats = (
    df.groupby("location")["rainfall_mm"]
    .agg(
        Total="sum",
        Average="mean",
        Maximum="max",
        Dry_Days=lambda x: (x == 0).sum(),   # count of zero-rainfall readings
    )
    .round(2)
)

# ── 3c. Daily areal mean (arithmetic average across all stations per day) ────
daily_areal_mean = (
    df.groupby("date")["rainfall_mm"]
    .mean()
    .reset_index()
    .rename(columns={"rainfall_mm": "areal_mean_mm"})
)

# Identify the wettest single day (highest areal mean)
wettest_row   = daily_areal_mean.loc[daily_areal_mean["areal_mean_mm"].idxmax()]
wettest_date  = wettest_row["date"].date()
wettest_value = wettest_row["areal_mean_mm"]


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Print the summary report
#
# The report is structured in three sections:
#   (A) Overall basin summary
#   (B) Per-station breakdown
#   (C) Daily areal means
# ─────────────────────────────────────────────────────────────────────────────

WIDTH = 55   # column width for the report box

def divider(char="─"):
    print(char * WIDTH)

def header(title):
    print("\n" + "═" * WIDTH)
    print(f"  {title}")
    print("═" * WIDTH)

def row(label, value, unit=""):
    print(f"  {label:<30} {value:>10} {unit}")


# ── Section A: Overall summary ───────────────────────────────────────────────
header("RAINFALL SUMMARY REPORT")
print(f"  Generated : {date.today()}")
print(f"  Data file : {CSV_FILE}")
divider()

header("A. OVERALL BASIN STATISTICS")
row("Total rainfall",        f"{total_rainfall:.1f}",   "mm")
row("Average per reading",   f"{average_rainfall:.2f}", "mm")
row("Maximum single reading",f"{max_rainfall:.1f}",     "mm")
row("Minimum single reading",f"{min_rainfall:.1f}",     "mm")
row("Rainy days (>0 mm)",    rainy_days,                "days")
row("Dry days (0 mm)",       dry_days,                  "days")
row("Wettest day (areal)",   f"{wettest_date}",         "")
row("  → areal mean",        f"{wettest_value:.2f}",    "mm")

# ── Section B: Per-station breakdown ─────────────────────────────────────────
header("B. PER-STATION BREAKDOWN")
print(f"  {'Station':<14} {'Total':>8} {'Average':>9} {'Maximum':>9} {'Dry Days':>9}")
divider()
for station, stats in location_stats.iterrows():
    print(
        f"  {station:<14} "
        f"{stats['Total']:>7.1f}mm "
        f"{stats['Average']:>8.2f}mm "
        f"{stats['Maximum']:>8.1f}mm "
        f"{int(stats['Dry_Days']):>7} d"
    )

# ── Section C: Daily areal means ─────────────────────────────────────────────
header("C. DAILY AREAL MEAN RAINFALL")
print(f"  {'Date':<14} {'Areal Mean':>12}   {'Bar chart (1 █ ≈ 2 mm)'}")
divider()
for _, r in daily_areal_mean.iterrows():
    val      = r["areal_mean_mm"]
    bar      = "█" * int(val / 2)          # simple ASCII bar chart
    marker   = " ← wettest" if r["date"].date() == wettest_date else ""
    print(f"  {str(r['date'].date()):<14} {val:>8.2f} mm   {bar}{marker}")

divider()
print("  [End of Report]")
print("═" * WIDTH + "\n")
