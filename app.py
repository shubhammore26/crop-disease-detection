from flask import Flask, render_template, request
import os
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "static/uploads"
MODEL_PATH = "model/crop_model.h5"
IMAGE_SIZE = 224

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- LOAD MODEL ----------------
model = tf.keras.models.load_model(MODEL_PATH)

# IMPORTANT: CLASS ORDER MUST MATCH check_classes.py
CLASS_NAMES = [
    "Pepper (Healthy)",
    "Potato (Early Blight)",
    "Tomato (Bacterial Spot)",
    "Tomato (Healthy)"
]

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    image_url = None
    prediction = None
    message = None

    if request.method == "POST":
        image = request.files.get("image")

        if image and image.filename != "":
            # Save image
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            image_url = image_path
            message = "Image uploaded successfully"

            # Preprocess image
            img = Image.open(image_path).convert("RGB")
            img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            preds = model.predict(img_array)
            prediction = CLASS_NAMES[np.argmax(preds)]

    return render_template(
        "index.html",
        image_url=image_url,
        prediction=prediction,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
