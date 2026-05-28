from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.api.rank import (
    router as rank_router,
)

app = FastAPI(
    title="Quant Engine"
)

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================================
# ROUTES
# =========================================

app.include_router(
    rank_router
)

# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message":
        "Quant Engine Running"
    }