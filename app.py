"""Flask entry point for the interactive bit-shift lesson."""
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.get('/')
    def index():
        return render_template('index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5177, debug=False)
