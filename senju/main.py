from __future__ import annotations

from pathlib import Path

from flask import (Flask, redirect, render_template, request, url_for,
                   send_from_directory)

from senju.haiku import Haiku
from senju.store_manager import StoreManager

import os

app = Flask(__name__)

store = StoreManager(Path("/tmp/store.db"))


def foobar():
    """WE KNOW"""
    a = 3
    b = 3
    return a + b


@app.route("/")
def index_view():
    return render_template("index.html", title="Senju")


@app.route("/haiku/")
def haiku_index_view():
    haiku_id: int | None = store.get_id_of_latest_haiku()
    if haiku_id is None:
        # TODO: add "empty haiku list" error page
        raise KeyError("no haiku exist yet")
    return redirect(url_for("haiku_view", haiku_id=haiku_id))


@app.route("/haiku/<int:haiku_id>")
def haiku_view(haiku_id):
    """test"""
    haiku: Haiku | None = store.load_haiku(haiku_id)
    if haiku is None:
        # TODO: add "haiku not found" page
        raise KeyError("haiku not found")
    context: dict = {
        "haiku": haiku
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


@app.route("/api/v1/haiku", methods=['POST'])
def generate_haiku():
    if request.method == 'POST':
        json_data = request.get_json()
        prompt = json_data["prompt"]
        if len(prompt)>100:
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
