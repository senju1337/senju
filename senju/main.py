from __future__ import annotations

import os
from pathlib import Path

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

from senju.haiku import Haiku
from senju.store_manager import StoreManager

app = Flask(__name__)

store = StoreManager(Path("/tmp/store.db"))


def foobar():
    """WE KNOW"""
    a = 3
    b = 3
    return a + b


@app.route("/")
def index_view():
    """
    Render the main index page of the application.

    Returns:
        Text: The index.html template with title "Senju".
    """

    return render_template("index.html", title="Senju")


@app.route("/haiku/")
def haiku_index_view():
    """
    Redirect to the most recently created haiku.

    Returns:
        Response: Redirects to the haiku_view route with the latest haiku ID.

    Raises:
        KeyError: If no haikus exist in the store yet.
    """

    haiku_id: int | None = store.get_id_of_latest_haiku()
    if haiku_id is None:
        # TODO: add "empty haiku list" error page
        raise KeyError("no haiku exist yet")
    return redirect(url_for("haiku_view", haiku_id=haiku_id))


@app.route("/haiku/<int:haiku_id>")
def haiku_view(haiku_id):
    """
    Display a specific haiku by its ID.

    Loads the haiku with the given ID from the store and renders it using
    the haiku.html template. If no haiku is found with the provided ID,
    raises a KeyError.

    Args:
        haiku_id (int): The ID of the haiku to display.

    Returns:
        Text: The haiku.html template with the haiku data in context.

    Raises:
        KeyError: If no haiku exists with the given ID.
    """

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
    """
    Render the haiku generation prompt page.

    Returns:
        Text: The prompt.html template with title "Haiku generation".
    """

    return render_template(
        "prompt.html",
        title="Haiku generation"
    )


@app.route("/scan")
def scan_view():
    """
    Render the image scanning page.

    Returns:
        Text: The scan.html template with title "Image scanning".
    """
    return render_template(
        "scan.html",
        title="Image scanning"
    )


@app.route("/api/v1/haiku", methods=['POST'])
def generate_haiku():
    """
    API endpoint to generate a new haiku based on the provided prompt.

    Accepts POST requests with JSON data containing a 'prompt' field.
    Generates a haiku using the prompt, saves it to the store,
    and returns the ID.

    Returns:
        str: The ID of the newly created haiku if method is POST.
        tuple: Error message and status code 405 if method is not POST.
    """

    if request.method == 'POST':
        json_data = request.get_json()
        prompt = json_data["prompt"]
        haiku = Haiku.request_haiku(prompt)
        id = store.save_haiku(haiku)
        return str(id)
    else:
        return "Method not allowed", 405


@app.route('/favicon.ico')
def favicon():
    """
    Serve the favicon.ico file from the static directory.

    Returns:
        Response: The favicon.ico file with the appropriate MIME type.
    """

    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
