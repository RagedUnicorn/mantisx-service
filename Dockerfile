FROM python:3-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD ["--days-back", "7", "--output-dir", "sessions"]
