from contextlib import asynccontextmanager
from fastapi import FastAPI
from transformers import (
    AutoImageProcessor,
    AutoModel,
)

import src.config as config

from src.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models during startup

    app.state.model = AutoModel.from_pretrained(
        config.MODEL_ID,
        trust_remote_code=True,
        low_cpu_mem_usage=True,  # Activates memory-efficient loading
        device_map="auto",  # Distributes layers across devices
    )

    app.state.preprocessor = AutoImageProcessor.from_pretrained(
        config.MODEL_ID,
        trust_remote_code=True,
        use_fast=True,
    )

    yield

    # Cleanup during shutdown (e.g., GPU memory)
    del app.state.model
    del app.state.preprocessor


app = FastAPI(
    description="Mushrooms Classification API", version="0.1.0", lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Welcome to Mushrooms Classification API 🍄"}


app.include_router(router)
