# Quantitative Momentum Research Platform

Institutional-style momentum analytics engine for ranking and validating NIFTY 500 stocks using rolling factor models, weighted momentum scoring, and forward validation analytics.

---

## Overview

This platform is a quantitative equity research system designed to analyze the NIFTY 500 universe using rolling momentum-based factor models.

The engine computes weighted multi-week momentum scores, ranks the strongest equities, and validates momentum persistence using future out-of-sample performance windows.

The project combines:

* Quantitative finance
* Data engineering
* Backend systems
* Financial analytics
* Interactive dashboarding

---

# Features

## Rolling Momentum Ranking Engine

* Analyze NIFTY 500 stocks using rolling 4-week windows
* Dynamically shift analysis windows forward/backward
* Custom rolling window selection
* Newest-to-oldest weighted scoring system

---

## Weighted Momentum Scoring

Recent periods receive higher importance.

Example weighting:

| Week        | Weight |
| ----------- | ------ |
| Most Recent | 4      |
| Week 2      | 3      |
| Week 3      | 2      |
| Oldest      | 1      |

---

## Consistency-Based Ranking

The engine rewards:

* More positive-return periods
* Consistent momentum
* Stable trend continuation

instead of favoring only high volatility spikes.

---

## Future Validation Analytics

After ranking the top equities, the system computes:

* Future Week +1 return
* Future Week +2 return

These are NOT included in ranking calculations.

They are used for:

* momentum persistence analysis
* out-of-sample validation
* factor research evaluation

---

## Historical Data Pipeline

* Fetches NIFTY 500 OHLC data using Zerodha APIs
* Stores historical data locally
* Incremental updates only
* Avoids redundant downloads
* Supports multi-year datasets

---

## Interactive Institutional Dashboard

Features:

* Rolling week timeline
* Dynamic week selection
* Interactive rolling windows
* Forward/backward shifting
* Compact research-focused tables
* CSV export support

---

# Architecture

```txt
Frontend (Next.js + TypeScript)
        ↓
FastAPI Backend
        ↓
Ranking Engine (Pandas)
        ↓
Historical Data Store (CSV/PostgreSQL)
        ↓
Zerodha Market Data APIs
```

---

# Tech Stack

## Frontend

* Next.js
* React
* TypeScript
* TailwindCSS
* Axios

## Backend

* FastAPI
* Python
* Pandas
* Pydantic

## Data

* Zerodha Kite API
* CSV-based caching
* PostgreSQL (optional)

---

# Ranking Methodology

## Step 1 — Rolling Window Creation

The user selects any anchor week.

The system automatically creates:

```txt
[A B C D]
```

Where:

* A = newest week
* D = oldest week

---

## Step 2 — Weekly Return Computation

Weekly return formula:

\text{Return} = \frac{(\text{Close} - \text{Open})}{\text{Open}} \times 100

---

## Step 3 — Weighted Scoring

More recent weeks receive higher weights.

Example:

```txt
Week A → Weight 4
Week B → Weight 3
Week C → Weight 2
Week D → Weight 1
```

---

## Step 4 — Consistency Bonus

Stocks with more positive-return weeks receive additional score bonuses.

This rewards:

* trend persistence
* smoother momentum
* reduced noise

---

## Step 5 — Future Validation

The engine computes:

```txt
Future Week +1
Future Week +2
```

to evaluate whether momentum persisted after ranking.

---

# Example Workflow

## Select Rolling Window

```txt
[ Current Week ]
[ Previous Week ]
[ Week -2 ]
[ Week -3 ]
```

---

## Compute Rankings

The engine:

* computes weighted momentum scores
* ranks top 10 equities
* calculates consistency metrics
* generates future validation returns

---

## Export Results

Export rankings directly as CSV.

---

# Project Structure

```txt
backend/
│
├── app/
│   ├── api/
│   │   └── rank.py
│   │
│   ├── services/
│   │   ├── market_data.py
│   │   └── ranking.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   └── main.py
│
├── data/
│   ├── historical_data.csv
│   └── nifty500_symbols.csv
│
└── requirements.txt


frontend/
│
├── app/
│   └── page.tsx
│
├── components/
│
└── package.json
```

---

# Installation

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Start Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```txt
http://127.0.0.1:8000
```

---

# Frontend Setup

## Install Dependencies

```bash
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend runs on:

```txt
http://localhost:3000
```

---

# API Example

## POST `/rank`

### Request

```json
{
  "start_date": "2026-02-01",
  "end_date": "2026-02-28"
}
```

---

### Response

CSV containing:

* Top 10 ranked equities
* Weekly momentum returns
* Weighted scores
* Consistency metrics
* Future validation returns

---

# Future Improvements

## Planned Enhancements

* Strategy backtesting engine
* Portfolio simulation
* Sector-relative momentum
* Volatility-adjusted ranking
* Redis caching
* PostgreSQL historical storage
* AI research assistant
* Live paper trading
* Docker deployment
* AWS deployment
* Factor blending models
* Portfolio optimization
* ML prediction models

---

# Why This Project Matters

This project demonstrates:

* Quantitative finance concepts
* Rolling factor research
* Data engineering workflows
* Backend architecture design
* Financial analytics
* Large-scale computation pipelines
* Institutional dashboard design

---

# License

MIT License

---

# Author

Anish Balabattuni

