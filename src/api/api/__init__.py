from flask import Flask
import logging


def create_app():
    app = Flask(__name__)
    from . import get_article
    app.register_blueprint(get_article.bp)
    init_logging()
    return app


def init_logging():
    """Initializes logging."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")
