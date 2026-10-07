import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input

# The model is loaded once so repeated predictions are faster.
MODEL = MobileNetV2(weights="imagenet")


def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))

    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)

    predictions = MODEL.predict(image_array, verbose=0)
    decoded = decode_predictions(predictions, top=3)[0]

    results = []
    for _, label, score in decoded:
        results.append({
            "label": label.replace("_", " ").title(),
            "confidence": round(float(score) * 100, 2)
        })

    return results
