from flask import Flask
import logging
import api.get_article as get_article

def create_app():
    app = Flask(__name__)
    app.register_blueprint(get_article.bp)
    init_logging()
    return app


def init_logging():
    """Initializes logging."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")
