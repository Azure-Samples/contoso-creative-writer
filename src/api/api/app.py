import os
from api.__init__ import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8080)