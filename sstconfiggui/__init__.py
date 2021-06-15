from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"

    # a simple page that says hello
    @app.route("/")
    def index():
        return render_template(
            "index.html",
            elements="""Lol"""
        )

    return app
