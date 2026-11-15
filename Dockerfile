FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install requirements + bleeding-edge yt-dlp with browser impersonation
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -U --pre "yt-dlp[default,curl-cffi]"

COPY . .

RUN mkdir -p /tmp/pulseclip_jobs static/clips

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
