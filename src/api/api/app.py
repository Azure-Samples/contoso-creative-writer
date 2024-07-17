from dotenv import load_dotenv
from os import getenv
load_dotenv()

# Instrument flask HTTP calls
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument(enable_commenter=True, commenter_options={})

from flask import Flask
import api.get_article as get_article
from api.logging import init_logging

# Where to mount the API, defaults to root
url_prefix = getenv("API_PREFIX")

# Where are we serving the UI static files from? Defaults to not serving them.
ui_folder = getenv("UI_FOLDER")

app = Flask(__name__, static_url_path='', static_folder=ui_folder)
app.register_blueprint(get_article.bp, url_prefix=url_prefix)
init_logging(sampling_rate=1.0)

if ui_folder:
    @app.route('/')
    def hello_world():
        return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)