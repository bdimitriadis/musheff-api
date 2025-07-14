import io
import logging

from fastapi import APIRouter, HTTPException, status, UploadFile, Depends
from PIL import Image

from src.dependencies import get_model, get_preprocessor
from src.schema import MushroomClassification
from src.services import classify_mushroom_in_image_svc


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/classify", response_model=MushroomClassification, status_code=status.HTTP_200_OK
)
async def classify_mushroom_in_image(
    image_file: UploadFile,
    model=Depends(get_model),
    preprocessor=Depends(get_preprocessor),
):
    """Open uploaded image file and call mushroom classification
    service.

    :param image_file: the uploaded image file
    :type image_file: UploadFile
    :param model: the pretrained model, defaults to Depends(get_model)
    :type model: PreTrainedModel, optional
    :param preprocessor: the preprocessor for image input transforms, defaults to Depends(get_preprocessor)
    :type preprocessor: BaseImageProcessor, optional
    :raises HTTPException: Internal Server Error in case of model/preprocessor loading failure or some uknown error,
    or Bad Request Error in case of corrupted or invalid uploaded file
    :return: mushroom_type, toxicity_profile, classification_confidence
    :rtype: MushroomClassification
    """
    logger.info(f"Classify image: {image_file.filename}")

    try:
        request_object_content = await image_file.read()
        img = Image.open(io.BytesIO(request_object_content))
        if img.mode != "RGB":
            img = img.convert("RGB")
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded file. The file may be corrupted or invalid.",
        )

    # Get class_name predicted and prediction probability
    class_name, toxicity, confidence = await classify_mushroom_in_image_svc(
        img, model, preprocessor
    )
    return MushroomClassification(
        mushroom_type=class_name, toxicity_profile=toxicity, confidence=confidence
    )
