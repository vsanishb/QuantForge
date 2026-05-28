import pandas as pd

from app.core.config import (
    HISTORICAL_FILE,
)

# =========================================
# LOAD HISTORICAL DATA
# =========================================

def load_historical_data():

    if not HISTORICAL_FILE.exists():

        return pd.DataFrame()

    return pd.read_csv(
        HISTORICAL_FILE
    )

# =========================================
# SAVE HISTORICAL DATA
# =========================================

def save_historical_data(df):

    df = df.drop_duplicates(
        subset=[
            "date",
            "symbol",
        ]
    )

    df = df.sort_values(
        ["symbol", "date"]
    )

    df.to_csv(
        HISTORICAL_FILE,
        index=False
    )