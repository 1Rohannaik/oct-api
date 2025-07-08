# Use a lightweight Python base image
FROM python:3.10-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
