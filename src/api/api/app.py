from dotenv import load_dotenv
load_dotenv()

# Instrument flask HTTP calls
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument(enable_commenter=True, commenter_options={})

from flask import Flask
import api.get_article as get_article
from api.logging import init_logging

app = Flask(__name__)
app.register_blueprint(get_article.bp)
init_logging(sampling_rate=1.0)

if __name__ == '__main__':
    app.run(debug=True, port=8080)