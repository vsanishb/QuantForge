import time
import pandas as pd

from datetime import (
    datetime,
    timedelta,
)

from kiteconnect import (
    KiteConnect,
)

from app.core.config import (
    API_KEY,
    ACCESS_TOKEN,
    SYMBOLS_FILE,
)

from app.services.storage import (
    load_historical_data,
    save_historical_data,
)

# =========================================
# INIT KITE
# =========================================

kite = KiteConnect(
    api_key=API_KEY
)

kite.set_access_token(
    ACCESS_TOKEN
)

# =========================================
# LOAD SYMBOLS
# =========================================

def load_symbols():

    df = pd.read_csv(
        SYMBOLS_FILE,
        header=None
    )

    return (
        df[0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

# =========================================
# FETCH DATA
# =========================================

def update_market_data():

    existing_df = (
        load_historical_data()
    )

    # -------------------------------------
    # FIRST RUN
    # -------------------------------------

    if existing_df.empty:

        from_date = (
            datetime.now() -
            timedelta(days=365)
        )

    else:

        existing_df["date"] = (
            pd.to_datetime(
                existing_df["date"]
            )
        )

        latest_date = (
            existing_df["date"]
            .max()
        )

        from_date = (
            latest_date +
            timedelta(days=1)
        )

    to_date = datetime.now()

    # -------------------------------------
    # NO UPDATE NEEDED
    # -------------------------------------

    if from_date.date() >= to_date.date():

        print(
            "Historical data already updated"
        )

        return existing_df

    print(
        f"Updating data from {from_date.date()} to {to_date.date()}"
    )

    symbols = load_symbols()

    instruments = (
        kite.instruments("NSE")
    )

    instrument_df = (
        pd.DataFrame(
            instruments
        )
    )

    token_map = dict(
        zip(
            instrument_df[
                "tradingsymbol"
            ],

            instrument_df[
                "instrument_token"
            ]
        )
    )

    new_data = []

    for symbol in symbols:

        try:

            if symbol not in token_map:
                continue

            token = token_map[
                symbol
            ]

            candles = (
                kite.historical_data(
                    instrument_token=token,

                    from_date=from_date.strftime(
                        "%Y-%m-%d"
                    ),

                    to_date=to_date.strftime(
                        "%Y-%m-%d"
                    ),

                    interval="day"
                )
            )

            if not candles:
                continue

            df = pd.DataFrame(
                candles
            )

            df["symbol"] = symbol

            new_data.append(df)

            print(
                f"Updated: {symbol}"
            )

            time.sleep(0.15)

        except Exception as e:

            print(
                f"Failed: {symbol}"
            )

            print(e)

    # -------------------------------------
    # NO NEW DATA
    # -------------------------------------

    if len(new_data) == 0:

        return existing_df

    new_df = pd.concat(
        new_data,
        ignore_index=True
    )

    final_df = pd.concat(
        [
            existing_df,
            new_df,
        ],
        ignore_index=True
    )

    save_historical_data(
        final_df
    )

    return final_df