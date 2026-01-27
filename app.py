from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        image = request.files.get("image")

        if image:
            # For now, just confirm upload
            return render_template(
                "index.html",
                message="Image uploaded successfully"
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
