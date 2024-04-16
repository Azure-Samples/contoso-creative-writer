import os
import prompty
from api import create_app, get_article
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)