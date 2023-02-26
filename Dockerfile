# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set command to start app
CMD ["python", "app.py"]
