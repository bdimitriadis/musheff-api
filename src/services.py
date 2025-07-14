import logging

from typing import Tuple

import torch

from fastapi import HTTPException, status
from PIL import Image
from transformers import PreTrainedModel
from transformers.image_processing_utils import BaseImageProcessor


logger = logging.getLogger(__name__)


async def classify_mushroom_in_image_svc(
    img: Image.Image, model: PreTrainedModel, preprocessor: BaseImageProcessor
) -> Tuple[str, str, str]:
    """Service used to classify a mushroom shown in an image.
    The mushroom is classified to one of many well known mushroom classes/types,
    as well as according to its toxicity profile (i.e. edible or poisonous).
    Additionally, a probability is returned showing confidence of classification.

    :param img: the input image of the mushroom to be classified
    :type img: Image.Image
    :param model: the pretrained model
    :type model: PretrainedModel
    :param preprocessor: the auto preprocessor for image transforms (rescales, crops, normalizations etc.)
    :type preprocessor: BaseImageProcessor
    :raises HTTPException: Internal Server Error
    :return: mushroom_type, toxicity_profile, classification_confidence
    :rtype: Tuple[str, str, float]
    """

    try:

        logger.debug("Loading classification model.")

        inputs = preprocessor(img, return_tensors="pt").to(model.device)

        # Turn on model evaluation mode and inference mode
        model.eval()
        with torch.inference_mode():
            logger.debug("Starting classification process...")

            # Make a prediction on image with an extra dimension and send it to the target device
            target_image_pred = model(inputs["pixel_values"])

        # Convert logits -> prediction probabilities (using torch.softmax() for multi-class classification)
        target_image_pred_probs = torch.softmax(target_image_pred, dim=1)

        # model predicts one of the 12 potential mushroom classes
        predicted_label = target_image_pred.argmax(dim=1).item()

        # Get the label/class name of the prediction made using id2label
        class_name = model.config.id2label[predicted_label]

        # Split class_name to mushroom type and toxicity profile
        class_type, toxicity = class_name.rsplit("_", 1)

        # 4 decimal points precision
        prob = round(target_image_pred_probs.max().item(), 4)

        logger.debug("Finished classification process...")
        return class_type, toxicity, prob

    except Exception as e:
        logger.error(f"Classification process error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Classification process failed due to an internal error. Contact support if this persists.",
        )
