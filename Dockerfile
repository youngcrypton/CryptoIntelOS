# ==========================================
# CryptoIntel OS
# Production Docker Image
# ==========================================

FROM python:3.13-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is unbuffered
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install required Linux packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxfixes3 \
    libx11-xcb1 \
    libxcb1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (better Docker layer caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser
RUN playwright install chromium

# Copy the project
COPY . .

# Expose application directory
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "src"]