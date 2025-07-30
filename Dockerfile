# Use slim Python 3.10 base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --upgrade pip \
 && pip list  # Optional: helps debug what’s installed

# Copy project files (including tools/, app.py, etc.)
COPY . .

# Expose the Gradio port
EXPOSE 7860

# Run the app
CMD ["python3", "app.py"]
