from __future__ import annotations

from pathlib import Path

from flask import (Flask, redirect, render_template, request, url_for,
                   send_from_directory)

from senju.haiku import Haiku
from senju.image_reco import gen_response
from senju.store_manager import StoreManager

import os

app = Flask(__name__)

store = StoreManager(Path("/tmp/store.db"))


@app.route("/")
def index_view():
    return render_template("index.html", title="Senju")


@app.route("/haiku/")
def haiku_index_view():
    haiku_id: int | None = store.get_id_of_latest_haiku()
    if haiku_id is None:
        haiku_id = 0
    return redirect(url_for("haiku_view", haiku_id=haiku_id, is_default=1))


@app.route("/haiku/<int:haiku_id>")
def haiku_view(haiku_id):
    """test"""
    is_default: bool = request.args.get("is_default") == "1"
    haiku: Haiku = store.load_haiku(haiku_id)
    context: dict = {
        "haiku": haiku,
        "is_default": is_default
    }

    return render_template(
        "haiku.html",
        context=context,
        title="Haiku of the Day")


@app.route("/prompt")
def prompt_view():
    return render_template(
        "prompt.html",
        title="Haiku generation"
    )


@app.route("/scan")
def scan_view():
    return render_template(
        "scan.html",
        title="Image scanning"
    )


@app.route("/api/v1/image_reco", methods=['POST'])
def image_recognition():
    # note that the classifier is a singleton
    if 'image' not in request.files:
        return "No image file provided", 400

    image_file = request.files['image']
    image_data = image_file.read()

    try:
        results = gen_response(image_data)
        return results
    except Exception as e:
        return str(e), 500


@app.route("/api/v1/haiku", methods=['POST'])
def generate_haiku():
    if request.method == 'POST':
        json_data = request.get_json()
        prompt = json_data["prompt"]
        if len(prompt) > 100:
            return "Content Too Large", 413
        haiku = Haiku.request_haiku(prompt)
        id = store.save_haiku(haiku)
        return str(id)
    else:
        return "Method not allowed", 405


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
