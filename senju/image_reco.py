import torch
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageDescriptionGenerator:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        """
        Initialize an image description generator using a vision-language
        model.

        Args:
            model_name: The name of the model to use
                        (default: BLIP captioning model)
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def generate_description(self, image_data, max_length=50):
        """
        Generate a descriptive caption for the given image.

        Args:
            image_data: Raw image data (bytes)
            max_length: Maximum length of the generated caption

        Returns:
            dict: A dictionary containing the generated description
            and confidence score
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


g_descriptor:  ImageDescriptionGenerator = ImageDescriptionGenerator()


def gen_response(image_data) -> dict:
    return g_descriptor.generate_description(image_data)
