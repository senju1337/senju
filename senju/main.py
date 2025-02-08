from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    context = {
        "number": 1337
    }
    return render_template("index.jinja", context=context, title="Senju")
