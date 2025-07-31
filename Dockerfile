FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt && pip install --upgrade pip

COPY . .

EXPOSE 7860

CMD ["python3", "app.py"]
