from flask import Flask, render_template

app = Flask(__name__)

urls = {
        "home": "index_view",
        "haiku":"haiku_view"
    }

@app.route("/")
def index_view():
    return render_template("index.jinja", title="Senju", urls=urls)


@app.route("/haiku")
def haiku_view():

    return render_template(
        "haiku.jinja",
        title="Haiku of the Day",
        urls = urls)
