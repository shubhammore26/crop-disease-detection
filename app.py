from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    image_url = None

    if request.method == "POST":
        image = request.files.get("image")

        if image:
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            image_url = image_path

            return render_template(
                "index.html",
                message="Image uploaded successfully",
                image_url=image_url
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
