FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --upgrade pip

# Copy all app source code
COPY . .

# Copy environment file explicitly
# COPY .env .env

# Expose Gradio port
EXPOSE 7860

# Start the app
CMD ["python3", "app.py"]
