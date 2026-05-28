from pathlib import Path

# =========================================
# BASE PATHS
# =========================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)

DATA_DIR = (
    BASE_DIR / "data"
)

DATA_DIR.mkdir(
    exist_ok=True
)

# =========================================
# FILES
# =========================================

SYMBOLS_FILE = (
    DATA_DIR /
    "nifty500_symbols.csv"
)

HISTORICAL_FILE = (
    DATA_DIR /
    "historical_data.csv"
)

TOP20_FILE = (
    DATA_DIR /
    "top20_rankings.csv"
)

# =========================================
# API CONFIG
# =========================================

API_KEY = (
    ""
)

ACCESS_TOKEN = (
    ""
)

# =========================================
# RANKING ENGINE CONFIG
# =========================================

# -----------------------------
# TOP RESULTS
# -----------------------------

TOP_N = 10

# -----------------------------
# CONSISTENCY BONUS
# -----------------------------

CONSISTENCY_MULTIPLIER = 10

# -----------------------------
# MAX LOOKBACK RANGE
# -----------------------------

MAX_LOOKBACK_DAYS = 365

# -----------------------------
# MAX SHIFT ALLOWED
# -----------------------------

MAX_SHIFT_WEEKS = 52

# =========================================
# DEFAULT TIMEFRAME DAYS
# =========================================

TIMEFRAME_DAYS = {

    "1w": 7,

    "2w": 14,

    "1m": 30,

    "3m": 90,

    "6m": 180,

    "1y": 365,
}

# =========================================
# DATE FORMATS
# =========================================

DATE_FORMAT = (
    "%Y-%m-%d"
)

DISPLAY_DATE_FORMAT = (
    "%d/%m/%y"
)

# =========================================
# CSV EXPORT CONFIG
# =========================================

CSV_FILENAME = (
    "top10_rankings.csv"
)

# =========================================
# UI / TABLE CONFIG
# =========================================

DEFAULT_SHIFT = 0

DEFAULT_TIMEFRAME = "1m"