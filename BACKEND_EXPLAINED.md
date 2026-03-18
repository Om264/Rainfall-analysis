# 🐍 Understanding the Backend Code
### `rainfall_analysis.py` — Explained for High School Students

---

## What is the "Backend"?

Think of an app like a restaurant. The **backend** is everything happening in
the kitchen — chopping vegetables, cooking, calculating the bill. You never
see it directly, but it does all the real work.

In our project, the backend is the Python script `rainfall_analysis.py`. It:
- Prepares the data (like a chef preparing ingredients)
- Does all the maths (adding up rainfall, finding averages)
- Produces a finished report (the meal served to the customer)

The frontend (the web page) is the dining room — it shows everything
beautifully, but it relies on the backend to have done the hard work first.

---

## The Big Picture: What Does the Script Actually Do?

Imagine you are a water scientist who has placed three rain gauges (measuring
sticks for rain) in different parts of a river valley. Every day for a week,
each gauge records how many millimetres of rain fell. You now have 21 numbers
spread across three locations and seven days.

The script takes those numbers, organises them, does the maths, and prints
a neat scientific report — automatically, in under a second.

Here is a map of the whole journey:

```
┌─────────────────────────────────────────────────────────────────┐
│                     WHAT THE SCRIPT DOES                        │
│                                                                  │
│  STEP 1          STEP 2          STEP 3          STEP 4         │
│  --------        --------        --------        --------       │
│  Create          Read the        Calculate       Print the      │
│  the CSV  ──▶   CSV with  ──▶   statistics ──▶  report         │
│  data file       pandas          & averages      to screen      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Creating the Data File

### What is a CSV?

A **CSV** (Comma-Separated Values) file is just a text file where data is
arranged in rows and columns — exactly like a spreadsheet, but saved as plain
text. You could open it in Excel, Google Sheets, or even Notepad.

Our CSV looks like this:

```
date,rainfall_mm,location
2024-06-01,12.4,Station_A
2024-06-01,8.7,Station_B
2024-06-01,15.0,Station_C
2024-06-02,0.0,Station_A
...
```

The first row is the **header** — it labels each column:
- `date` — which day was measured
- `rainfall_mm` — how many millimetres of rain fell
- `location` — which rain gauge recorded it

Every row after that is one reading from one station on one day.

### The Code

```python
import csv          # Python's built-in tool for reading/writing CSV files
import os           # Tools for working with files and folders
from datetime import date   # Lets us use today's date in the report

CSV_FILE = "rainfall_data.csv"   # The name we give our file
```

`import` is how Python loads extra tools. It's like picking up a specific
tool from a toolbox before you start a job. `csv`, `os`, and `datetime` are
all included with Python — no installation needed.

```python
sample_data = [
    ["2024-06-01", 12.4, "Station_A"],
    ["2024-06-01",  8.7, "Station_B"],
    # ... more rows
]
```

This is a **list of lists** — Python's way of storing a table. Each inner
list `[date, mm, location]` is one row of data.

```python
with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "rainfall_mm", "location"])
    writer.writerows(sample_data)
```

`open()` creates a new file and opens it for writing (`mode="w"`).
The `with` keyword means "open the file, do the work inside, then close it
safely — even if something goes wrong." This is good practice whenever
you work with files.

`writer.writerow(...)` writes one row. `writer.writerows(...)` writes many
rows at once from our list.

---

## Step 2 — Reading the CSV with pandas

### What is pandas?

**pandas** is one of the most popular Python libraries in the world for
working with data. It lets you load a spreadsheet into Python and then
slice, filter, group, and calculate with just a few words of code.

The central object in pandas is called a **DataFrame** — basically a table
with row and column labels, like an in-memory spreadsheet.

```
    df  (our DataFrame)
    ┌────────────┬─────────────┬────────────┐
    │   date     │ rainfall_mm │  location  │
    ├────────────┼─────────────┼────────────┤
    │ 2024-06-01 │    12.4     │ Station_A  │
    │ 2024-06-01 │     8.7     │ Station_B  │
    │ 2024-06-02 │     0.0     │ Station_A  │
    │  ...       │   ...       │  ...       │
    └────────────┴─────────────┴────────────┘
    21 rows × 3 columns
```

### The Code

```python
import pandas as pd

df = pd.read_csv(CSV_FILE, parse_dates=["date"])
```

`pd.read_csv()` reads the whole CSV file and turns it into a DataFrame
in one line. `parse_dates=["date"]` tells pandas to treat the `date`
column as actual calendar dates — not just plain text — so we can later
sort by date, find the earliest day, etc.

```python
print(df.head(5))          # Show the first 5 rows
print(df.shape)            # Show (rows, columns)
print(df['date'].min())    # Earliest date in the data
print(df['location'].unique())  # List of unique station names
```

`df.head(5)` is like peering at the top of the table. It is always a good
idea to check that your data loaded correctly before doing calculations.

---

## Step 3 — Calculating Statistics

This is where the maths happens. We calculate three levels of statistics:

### 3a — Overall basin statistics

```python
total_rainfall   = df["rainfall_mm"].sum()    # add up all readings
average_rainfall = df["rainfall_mm"].mean()   # arithmetic mean
max_rainfall     = df["rainfall_mm"].max()    # highest single reading
min_rainfall     = df["rainfall_mm"].min()    # lowest single reading
```

`df["rainfall_mm"]` picks just the rainfall column (imagine highlighting a
whole column in a spreadsheet). Then `.sum()`, `.mean()`, `.max()`, `.min()`
are built-in pandas functions that instantly compute those values across
all 21 rows.

```python
rainy_days = df[df["rainfall_mm"] > 0]["date"].nunique()
dry_days   = df[df["rainfall_mm"] == 0]["date"].nunique()
```

`df[df["rainfall_mm"] > 0]` is called **filtering** — it keeps only rows
where rainfall was greater than zero (just like using a filter in Excel).
`.nunique()` then counts how many *unique* dates appear in those filtered rows.

### 3b — Per-station statistics (groupby)

```python
location_stats = (
    df.groupby("location")["rainfall_mm"]
    .agg(
        Total   = "sum",
        Average = "mean",
        Maximum = "max",
        Dry_Days = lambda x: (x == 0).sum()
    )
    .round(2)
)
```

`.groupby("location")` is one of the most powerful pandas tools. It splits
the table into separate groups — one for Station_A, one for Station_B, one
for Station_C — and then applies the same calculation to each group.

Imagine sorting a deck of cards by suit, then counting each suit separately.
That is exactly what `groupby` does.

`.agg()` lets you run multiple calculations at once. Here we get Total,
Average, Maximum, and Dry_Days for every station in a single step.

### 3c — Daily areal mean

```python
daily_areal_mean = (
    df.groupby("date")["rainfall_mm"]
    .mean()
    .reset_index()
    .rename(columns={"rainfall_mm": "areal_mean_mm"})
)
```

This time we group by **date** instead of location. For each day, we average
the readings from all three stations to get one representative number for
the whole area. In hydrology this is called the **areal mean** — it answers
the question "how much did it rain across the whole catchment on this day?"

```python
wettest_row  = daily_areal_mean.loc[daily_areal_mean["areal_mean_mm"].idxmax()]
wettest_date = wettest_row["date"].date()
```

`.idxmax()` finds the *index* (row number) of the highest value.
`.loc[...]` then retrieves that specific row. This is how we find the
wettest single day automatically, no matter how large the dataset is.

---

## Step 4 — Printing the Report

```python
def header(title):
    print("\n" + "═" * 55)
    print(f"  {title}")
    print("═" * 55)

def row(label, value, unit=""):
    print(f"  {label:<30} {value:>10} {unit}")
```

These are **functions** — small, reusable blocks of code. Instead of
writing the same print formatting code over and over, we define it once
and call it whenever we need it.

`"═" * 55` repeats the `═` character 55 times — a quick way to draw a
horizontal line.

`f"  {label:<30} {value:>10} {unit}"` is an **f-string** (formatted string).
The `<30` means "pad with spaces so the label takes up exactly 30 characters,
left-aligned." The `>10` means "right-align the value in 10 characters."
This makes all the numbers line up neatly in columns.

The ASCII bar chart:

```python
bar = "█" * int(val / 2)
```

This is elegantly simple. If the daily average was 34.57 mm, then
`int(34.57 / 2)` = `17`, so we print 17 block characters: `█████████████████`.
Longer bar = more rain. No chart library needed — just one line of Python.

---

## How All Four Steps Connect

Here is the full flow from raw numbers to finished report:

```
                 YOUR DATA
               (21 rainfall readings)
                      │
                      ▼
        ┌─────────────────────────────┐
        │  STEP 1: Write to CSV       │
        │  csv.writer saves rows to   │
        │  rainfall_data.csv          │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  STEP 2: Read with pandas   │
        │  pd.read_csv() loads the    │
        │  table into a DataFrame     │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  STEP 3: Calculate          │
        │  .sum()  .mean()  .max()    │
        │  .groupby()  .idxmax()      │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  STEP 4: Print Report       │
        │  Sections A, B, C           │
        │  with ASCII bar chart       │
        └─────────────────────────────┘
```

---

## Key Concepts to Remember

| Concept | What it means | Real-life analogy |
|---------|--------------|------------------|
| **Variable** | A named box that holds a value | A labelled jar in a cupboard |
| **List** | A collection of items in order | A shopping list |
| **DataFrame** | A table of data in memory | A spreadsheet |
| **Function** | A reusable block of code | A recipe you can use again and again |
| **Filter** | Keeping only rows that match a condition | Sieving flour |
| **groupby** | Splitting data into groups then calculating | Sorting exam papers by class |
| **f-string** | A string that can include variable values | A fill-in-the-blanks template |
| **import** | Loading an extra tool/library | Picking a screwdriver from a toolbox |

---

## Try It Yourself — Mini Challenges

1. **Change the stations** — Add a fourth station called `Station_D` with
   your own rainfall values and re-run the script. What changes in the report?

2. **Find the driest station** — After Step 3, add this line and see what it prints:
   ```python
   print(location_stats["Total"].idxmin())
   ```

3. **Change the bar chart scale** — The bar currently uses 1 block per 2 mm.
   Edit `int(val / 2)` to `int(val / 5)`. How does the chart change?

4. **Save the report** — Run the script with this command and open the file:
   ```bash
   python rainfall_analysis.py > my_report.txt
   ```

---

*Well done for reading this far! You now understand how a real
water resources data pipeline works from start to finish.*
