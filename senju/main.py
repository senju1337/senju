from logging import Logger
from pathlib import Path
from flask import Flask, redirect, render_template, url_for

from senju.haiku import Haiku
from senju.store_manager import StoreManager

app = Flask(__name__)

store = StoreManager(Path("/tmp/store.db"))


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
