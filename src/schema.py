from pydantic import BaseModel


class MushroomClassification(BaseModel):
    mushroom_type: str
    toxicity_profile: str
    confidence: float
