from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    context = {
        "number": 1337
    }
    return render_template("index.jinja", context=context, title="Senju")
