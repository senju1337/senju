from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index_view():
    return render_template("index.jinja", title="Senju")


@app.route("/haiku")
def haiku_view():

    return render_template(
        "haiku.jinja",
        title="Haiku of the Day")
