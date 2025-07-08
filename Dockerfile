FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Env settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Set working dir
WORKDIR /app

# Copy and install deps
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy rest of app
COPY . .

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
