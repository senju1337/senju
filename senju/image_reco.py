import numpy as np
from PIL import Image
import keras
import io

g_model = None


class SimpleClassifier:
    def __init__(self):
        global g_model
        if g_model is None:
            g_model = keras.applications.MobileNetV2(weights="imagenet")
        self.model = g_model

    def classify(self, image_data):
        # Convert uploaded bytes to image
        img = Image.open(io.BytesIO(image_data)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Get predictions
        predictions = self.model.predict(img_array)
        results = keras.applications.mobilenet_v2.decode_predictions(
            predictions, top=5)[0]

        data: dict = {}
        all_labels: list[dict] = []
        data["best_guess"] = {"label": "", "confidence": float(0)}
        for _, label, score in results:
            score = float(score)
            datapoint = {"label": label, "confidence": score}
            all_labels.append(datapoint)
            if data["best_guess"]["confidence"] < score:
                data["best_guess"] = datapoint

        data["all"] = all_labels

        return data
