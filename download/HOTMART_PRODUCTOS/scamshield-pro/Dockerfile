FROM python:3.12-slim AS base

LABEL maintainer="Eddy Flores <eddyflores100@gmail.com>"
LABEL org.opencontainers.image.title="ScamShield Pro"
LABEL org.opencontainers.image.description="Self-hosted URL fraud & phishing detector"
LABEL org.opencontainers.image.source="https://github.com/eddyflores100-lang/scamshield-pro"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

RUN useradd -m -u 1000 scamshield && chown -R scamshield:scamshield /app
USER scamshield

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "scamshield.server:app", "--host", "0.0.0.0", "--port", "8000"]
