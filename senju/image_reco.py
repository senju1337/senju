"""
Senju Image Recognition Module
=============================

A module providing image description generation capabilities for the Senju haiku application.

This module leverages pre-trained vision-language models (specifically BLIP) to generate
textual descriptions of uploaded images. These descriptions can then be used as input
for the haiku generation process, enabling image-to-haiku functionality.

Classes
-------
ImageDescriptionGenerator
    The primary class responsible for loading the vision-language model
    and generating descriptions from image data.

Functions
---------
gen_response
    A helper function that wraps the description generation process
    for API integration.

Dependencies
------------
* torch: Deep learning framework required for model operations
* PIL.Image: Image processing capabilities
* io: Utilities for working with binary data streams
* transformers: Hugging Face's library providing access to pre-trained models

Implementation Details
---------------------
The module initializes a BLIP model (Bootstrapped Language-Image Pre-training)
which can understand visual content and generate natural language descriptions.
The implementation handles image loading, preprocessing, model inference,
and post-processing to return structured description data.
"""

import torch
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageDescriptionGenerator:
    """
    A class for generating textual descriptions of images using a vision-language model.

    This class handles the loading of a pre-trained BLIP model, image preprocessing,
    and caption generation. It provides an interface for converting raw image data
    into natural language descriptions that can be used for haiku inspiration.

    :ivar processor: The BLIP processor for handling image inputs
    :type processor: BlipProcessor
    :ivar model: The BLIP model for conditional text generation
    :type model: BlipForConditionalGeneration
    :ivar device: The computation device (CUDA or CPU)
    :type device: str
    """

    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        """
        Initialize an image description generator using a vision-language
        model.

        :param model_name: The name of the pre-trained model to use
        :type model_name: str
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def generate_description(self, image_data, max_length=50):
        """
        Generate a descriptive caption for the given image.

        This method processes the raw image data, runs inference with the BLIP model,
        and returns a structured response with the generated description.

        :param image_data: Raw binary image data
        :type image_data: bytes
        :param max_length: Maximum token length for the generated caption
        :type max_length: int
        :return: Dictionary containing the generated description and confidence score
        :rtype: dict
        """
        # Convert uploaded bytes to image
        img = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process the image
        inputs = self.processor(
            images=img, return_tensors="pt").to(self.device)

        # Generate caption
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=5,
                num_return_sequences=1,
                temperature=1.0,
                do_sample=False
            )

        # Decode the caption
        caption = self.processor.decode(output[0], skip_special_tokens=True)

        return {
            "description": caption,
            "confidence": None
        }


# Global instance of the description generator
g_descriptor: ImageDescriptionGenerator = ImageDescriptionGenerator()


def gen_response(image_data) -> dict:
    """
    Generate a description for an image using the global description generator.

    This function provides a simplified interface to the image description functionality
    for use in API endpoints.

    :param image_data: Raw binary image data
    :type image_data: bytes
    :return: Dictionary containing the image description and confidence information
    :rtype: dict
    :raises Exception: If image processing or description generation fails
    """
    return g_descriptor.generate_description(image_data)
