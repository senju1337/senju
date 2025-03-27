"""
Senju Haiku Web Application
===========================

A Flask-based web interface for generating, viewing, and managing haiku poetry.

This application provides a comprehensive interface between users
and an AI-powered
haiku generation service, with persistent storage capabilities.
Users can interact
with the system through both a web interface and a RESTful API.

Features
--------
* **Landing page**: Welcome interface introducing users to the Senju service
* **Browsing interface**: Gallery-style viewing of previously generated haikus
* **Prompt interface**: Text input system for generating haikus from seed text
* **Image scanning**: Experimental interface for creating haikus
    from visual inputs
* **RESTful API**: Programmatic access for integration with other services

Architecture
------------
The application implements a RESTful architecture using Flask's routing system
and template rendering. All user interactions are handled through
clearly defined
routes, with appropriate error handling for exceptional cases.

Dependencies
------------
* future.annotations: Enhanced type hint support
* os, Path: Filesystem operations for storage management
* Flask: Core web application framework
* Haiku: Custom class for poem representation and generation
* StoreManager: Database abstraction for persistence operations
* datetime: Datetime helper to facilitate Haiku of the day

Implementation
--------------
The module initializes both a Flask application instance and a StoreManager
with a configured storage location. All routes and view functions required
for the complete web interface are defined within this module.
"""

from __future__ import annotations

import os
import random
from datetime import date
from pathlib import Path

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

from senju.haiku import Haiku
from senju.image_reco import gen_response
from senju.store_manager import StoreManager

app = Flask(__name__)

store = StoreManager(Path("/tmp/store.db"))

stored_date = date.today()
random_number = 1


@app.route("/")
def index_view():
    """
    Render the main index page of the application.

    :return: The index.html template with title "Senju".
    :rtype: flask.Response
    """
    global stored_date
    global random_number

    if stored_date != date.today():
        random_number = random.randint(0, store.count_entries())
        stored_date = date.today()

    haiku: Haiku | None = store.load_haiku(random_number)
    if haiku is None:
        raise KeyError("haiku not found")
    context: dict = {
        "haiku": haiku,
    }

    return render_template("index.html", context=context,
                           title="Haiku of the day")


@app.route("/haiku/")
def haiku_index_view():
    """
    Redirect to the most recently created haiku.

    :return: Redirects to the haiku_view route with the latest haiku ID.
    :rtype: flask.Response
    :raises KeyError: If no haikus exist in the store yet.
    """
    haiku_id: int | None = store.get_id_of_latest_haiku()
    haiku_default = haiku_id is None
    if haiku_default:
        haiku_id = 0
    return redirect(url_for("haiku_view", haiku_id=haiku_id,
                            is_default=1 if haiku_default else 0))


@app.route("/haiku/<int:haiku_id>")
def haiku_view(haiku_id):
    """
    Display a specific haiku by its ID.

    Loads the haiku with the given ID from the store and renders it using
    the haiku.html template. If no haiku is found with the provided ID,
    raises a KeyError.

    :param haiku_id: The ID of the haiku to display.
    :type haiku_id: int
    :return: The haiku.html template with the haiku data in context.
    :rtype: flask.Response
    :raises KeyError: If no haiku exists with the given ID.
    """
    haiku: Haiku | None = store.load_haiku(haiku_id)
    if haiku is None:
        # TODO: add "haiku not found" page
        raise KeyError("haiku not found")
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
    """
    Render the haiku generation prompt page.

    :return: The prompt.html template with title "Haiku generation".
    :rtype: flask.Response
    """
    return render_template(
        "prompt.html",
        title="Haiku generation"
    )


@app.route("/scan")
def scan_view():
    """
    Render the image scanning page.

    :return: The scan.html template with title "Image scanning".
    :rtype: flask.Response
    """
    return render_template(
        "scan.html",
        title="Image scanning"
    )


@app.route("/api/v1/image_reco", methods=['POST'])
def image_recognition():
    """
    generate a description of an image

    :return: json formatted description
    :rtype: json
    """
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
    """
    API endpoint to generate a new haiku based on the provided prompt.

    Accepts POST requests with JSON data containing a 'prompt' field.
    Generates a haiku using the prompt, saves it to the store,
    and returns the ID.

    :return: The ID of the newly created haiku if method is POST.
             Error message and status code 405 if method is not POST.
    :rtype: Union[str, Tuple[str, int]]
    """
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
    """
    Serve the favicon.ico file from the static directory.

    :return: The favicon.ico file with the appropriate MIME type.
    :rtype: flask.Response
    """
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
