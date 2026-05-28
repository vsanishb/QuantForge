from fastapi import (
    APIRouter,
    HTTPException,
)

from fastapi.responses import (
    FileResponse,
)

from pydantic import (
    BaseModel,
)

from datetime import (
    datetime,
)

from app.core.config import (
    TOP20_FILE,
)

from app.services.market_data import (
    update_market_data,
)

from app.services.ranking import (
    compute_rankings,
)

router = APIRouter()

# =========================================
# REQUEST MODEL
# =========================================

class RankRequest(
    BaseModel
):

    start_date: str

    end_date: str

# =========================================
# RANK ROUTE
# =========================================

@router.post("/rank")

def rank_stocks(
    body: RankRequest
):

    try:

        # =================================
        # VALIDATE DATES
        # =================================

        try:

            start_date = (
                datetime.strptime(
                    body.start_date,
                    "%Y-%m-%d"
                )
            )

            end_date = (
                datetime.strptime(
                    body.end_date,
                    "%Y-%m-%d"
                )
            )

        except Exception:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Invalid date format"
                )
            )

        # =================================
        # VALIDATE RANGE
        # =================================

        if end_date < start_date:

            raise HTTPException(

                status_code=400,

                detail=(
                    "End date must be after start date"
                )
            )

        total_days = (
            end_date -
            start_date
        ).days

        if total_days > 365:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Maximum range is 1 year"
                )
            )

        # =================================
        # UPDATE MARKET DATA
        # =================================

        df = update_market_data()

        # =================================
        # COMPUTE RANKINGS
        # =================================

        ranking_df = (
            compute_rankings(

                df=df,

                start_date=start_date,

                end_date=end_date,
            )
        )

        # =================================
        # EMPTY CHECK
        # =================================

        if ranking_df.empty:

            raise HTTPException(

                status_code=404,

                detail=(
                    "No rankings generated"
                )
            )

        # =================================
        # SAVE CSV
        # =================================

        ranking_df.to_csv(

            TOP20_FILE,

            index=False
        )

        # =================================
        # RETURN CSV
        # =================================

        return FileResponse(

            TOP20_FILE,

            media_type="text/csv",

            filename=(
                "top10_rankings.csv"
            )
        )

    # =====================================
    # HTTP ERRORS
    # =====================================

    except HTTPException:

        raise

    # =====================================
    # VALUE ERRORS
    # =====================================

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)
        )

    # =====================================
    # UNKNOWN ERRORS
    # =====================================

    except Exception as e:

        print(
            "RANK ROUTE ERROR:",
            str(e)
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Internal ranking engine error"
            )
        )