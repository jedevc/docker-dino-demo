import os
from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE = os.getcwd()
UPLOADS = os.path.join(BASE, os.environ["UPLOADS_DIR"])


@app.route("/")
def index():
    return "Hello World (and dinosuars)!"


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file provided", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    out_filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOADS, out_filename))

    return redirect("/dinos/" + out_filename)


@app.route("/dinos/<path:filename>")
def dinos(filename):
    return send_from_directory(UPLOADS, filename)
