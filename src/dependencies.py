from fastapi import Request, HTTPException
from transformers import PreTrainedModel
from transformers.image_processing_utils import BaseImageProcessor


def get_model(request: Request) -> PreTrainedModel:
    if not hasattr(request.app.state, "model"):
        raise HTTPException(status_code=500, detail="Model not loaded")
    return request.app.state.model


def get_preprocessor(request: Request) -> BaseImageProcessor:
    if not hasattr(request.app.state, "preprocessor"):
        raise HTTPException(status_code=500, detail="Preprocessor not loaded")
    return request.app.state.preprocessor
