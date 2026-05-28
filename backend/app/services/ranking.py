import pandas as pd

from app.core.config import (
    TOP_N,
    CONSISTENCY_MULTIPLIER,
)

# =========================================
# CONSTANTS
# =========================================

ROLLING_WINDOW_WEEKS = 4

FUTURE_WEEKS = 2

# =========================================
# COMPUTE PERIOD RETURN
# =========================================

def compute_period_return(
    period_df
):

    period_df = (
        period_df
        .sort_values("date")
    )

    open_price = (
        period_df.iloc[0]["open"]
    )

    close_price = (
        period_df.iloc[-1]["close"]
    )

    period_return = (
        (
            close_price -
            open_price
        ) / open_price
    ) * 100

    return round(
        period_return,
        2
    )

# =========================================
# FORMAT LABEL
# =========================================

def format_period_label(
    period_df
):

    start_period = (
        pd.to_datetime(
            period_df.iloc[0]["date"]
        )
        .strftime(
            "%d/%m/%y"
        )
    )

    end_period = (
        pd.to_datetime(
            period_df.iloc[-1]["date"]
        )
        .strftime(
            "%d/%m/%y"
        )
    )

    return (
        f"{start_period} to {end_period}"
    )

# =========================================
# MAIN RANKING ENGINE
# =========================================

def compute_rankings(
    df,
    start_date,
    end_date,
):

    # =====================================
    # PREPARE DATA
    # =====================================

    df["date"] = pd.to_datetime(
        df["date"]
    )

    try:

        df["date"] = (
            df["date"]
            .dt.tz_localize(None)
        )

    except Exception:

        pass

    start_date = pd.to_datetime(
        start_date
    )

    end_date = pd.to_datetime(
        end_date
    )

    # =====================================
    # FILTER WINDOW DATA
    # =====================================

    filtered_df = df[
        (
            df["date"] >=
            start_date
        )
        &
        (
            df["date"] <=
            end_date
        )
    ]

    if filtered_df.empty:

        raise ValueError(
            "No market data found"
        )

    # =====================================
    # SORT
    # =====================================

    filtered_df = (
        filtered_df
        .sort_values(
            ["symbol", "date"]
        )
    )

    # =====================================
    # CREATE PERIODS
    # =====================================

    filtered_df["period"] = (
        filtered_df["date"]
        .dt.to_period("W")
        .astype(str)
    )

    df["period"] = (
        df["date"]
        .dt.to_period("W")
        .astype(str)
    )

    # =====================================
    # SELECTED PERIODS
    # =====================================

    selected_periods = sorted(
        filtered_df["period"]
        .unique()
    )

    # newest -> oldest

    selected_periods = (
        selected_periods[::-1]
    )

    if (
        len(selected_periods) <
        ROLLING_WINDOW_WEEKS
    ):

        raise ValueError(
            "Need at least 4 weeks"
        )

    selected_periods = (
        selected_periods[:4]
    )

    # =====================================
    # ALL PERIODS
    # =====================================

    all_periods = sorted(
        df["period"]
        .unique()
    )

    all_periods = (
        all_periods[::-1]
    )

    # =====================================
    # FUTURE PERIODS
    # =====================================

    newest_selected = (
        selected_periods[0]
    )

    newest_index = (
        all_periods.index(
            newest_selected
        )
    )

    future_periods = []

    for i in range(
        1,
        FUTURE_WEEKS + 1
    ):

        future_index = (
            newest_index - i
        )

        if future_index >= 0:

            future_periods.append(
                all_periods[
                    future_index
                ]
            )

        else:

            future_periods.append(
                None
            )

    # =====================================
    # WEIGHTS
    # =====================================

    period_weights = {}

    total_period_count = len(
        selected_periods
    )

    for i, period in enumerate(
        selected_periods,
        start=1
    ):

        period_weights[
            period
        ] = (
            total_period_count -
            i +
            1
        )

    # =====================================
    # SYMBOLS
    # =====================================

    symbols = (
        filtered_df["symbol"]
        .unique()
    )

    results = []

    # =====================================
    # MAIN LOOP
    # =====================================

    for symbol in symbols:

        stock_df = df[
            df["symbol"] == symbol
        ]

        result = {
            "symbol": symbol
        }

        raw_score = 0

        positive_periods = 0

        negative_periods = 0

        valid_stock = True

        # =================================
        # RANKING PERIODS
        # =================================

        for idx, period in enumerate(
            selected_periods,
            start=1
        ):

            period_df = stock_df[
                stock_df["period"] == period
            ].sort_values("date")

            if len(period_df) == 0:

                valid_stock = False

                break

            period_return = (
                compute_period_return(
                    period_df
                )
            )

            if period_return > 0:

                positive_periods += 1

            else:

                negative_periods += 1

            priority = (
                period_weights[
                    period
                ]
            )

            weighted_score = round(
                period_return *
                priority,
                2
            )

            raw_score += (
                weighted_score
            )

            result[
                f"period{idx}_return"
            ] = period_return

            result[
                f"period{idx}_priority"
            ] = priority

            result[
                f"period{idx}_score"
            ] = weighted_score

            result[
                f"period{idx}_label"
            ] = format_period_label(
                period_df
            )

        # =================================
        # FUTURE PERIODS
        # =================================

        for future_idx, future_period in enumerate(
            future_periods,
            start=1
        ):

            if future_period is None:

                result[
                    f"future{future_idx}_return"
                ] = "--"

                result[
                    f"future{future_idx}_label"
                ] = "No Future Week"

                continue

            future_df = stock_df[
                stock_df["period"] == future_period
            ].sort_values("date")

            if len(future_df) == 0:

                result[
                    f"future{future_idx}_return"
                ] = "--"

                result[
                    f"future{future_idx}_label"
                ] = "No Future Week"

                continue

            future_return = (
                compute_period_return(
                    future_df
                )
            )

            result[
                f"future{future_idx}_return"
            ] = future_return

            result[
                f"future{future_idx}_label"
            ] = format_period_label(
                future_df
            )

        # =================================
        # FINAL SCORE
        # =================================

        if valid_stock:

            consistency_bonus = round(
                positive_periods *
                CONSISTENCY_MULTIPLIER,
                2
            )

            adjusted_score = round(
                raw_score +
                consistency_bonus,
                2
            )

            result[
                "raw_score"
            ] = round(
                raw_score,
                2
            )

            result[
                "positive_periods"
            ] = (
                positive_periods
            )

            result[
                "negative_periods"
            ] = (
                negative_periods
            )

            result[
                "consistency_bonus"
            ] = (
                consistency_bonus
            )

            result[
                "total_score"
            ] = (
                adjusted_score
            )

            results.append(
                result
            )

    # =====================================
    # EMPTY CHECK
    # =====================================

    if len(results) == 0:

        raise ValueError(
            "No rankings generated"
        )

    # =====================================
    # DATAFRAME
    # =====================================

    ranking_df = pd.DataFrame(
        results
    )

    # =====================================
    # SORT
    # =====================================

    ranking_df = (
        ranking_df
        .sort_values(
            by=[
                "positive_periods",
                "total_score",
            ],
            ascending=False
        )
        .reset_index(drop=True)
    )

    # =====================================
    # FINAL RANK
    # =====================================

    ranking_df["rank"] = (
        ranking_df.index + 1
    )

    # =====================================
    # COLUMN ORDER
    # =====================================

    fixed_columns = [

        "rank",

        "symbol",

        "total_score",

        "raw_score",

        "consistency_bonus",

        "positive_periods",

        "negative_periods",
    ]

    dynamic_columns = [

        col
        for col in ranking_df.columns

        if col not in fixed_columns
    ]

    ranking_df = ranking_df[
        fixed_columns +
        dynamic_columns
    ]

    # =====================================
    # RETURN
    # =====================================

    return ranking_df.head(
        TOP_N
    )