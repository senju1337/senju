from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.jinja", title="Senju", active_page="home")


@app.route("/haiku")
def haiku_page():
    return render_template(
        "haiku.jinja",
        title="Haiku of the Day",
        active_page="haiku")
