FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-jdk \
    python3 \
    python3-pip \
    gcc \
    time \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

RUN useradd -m runner
USER runner

EXPOSE 8000

CMD ["uvicorn", "main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]