FROM python:3-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py", "--days-back", "7", "--output-dir", "sessions"]
