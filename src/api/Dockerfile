FROM  python:3.11-slim

WORKDIR /app
COPY requirements.txt .
# Remove this copy packages are public
COPY packages /app/packages


RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]