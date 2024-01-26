FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    python3-venv \
    git \
    vim \
    curl \
    zlib1g-dev \
    libjpeg-dev \
    ffmpeg \
    gcc \
    musl-dev \
    imagemagick \
    fonts-liberation\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app .
COPY /Configs/policy.xml /etc/ImageMagick-6/policy.xml

RUN curl https://ollama.ai/install.sh | sh
