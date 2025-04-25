import os
import asyncio
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configurable startup delay
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", 5))

app = FastAPI()


@app.get("/hello")
async def hello():
    logger.info("GET /hello called")
    return {"message": "Hello!"}


@app.get("/ready")
@app.get("/alive")
async def health_check():
    logger.info("Health check endpoint called")
    return {"message": "ok"}


@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting up... delaying for {STARTUP_DELAY} seconds")
    await asyncio.sleep(STARTUP_DELAY)
    logger.info("Startup complete")


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        logger.warning(f"HTTPException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as exc:
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

@app.get("/crash")
async def crash():
    raise ValueError("Simulated failure")
