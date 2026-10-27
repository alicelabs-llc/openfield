FROM python:3.12-slim
LABEL maintainer="Eddy Flores"
LABEL org.opencontainers.image.title="LeadHarvester"

# Playwright needs browser deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
COPY . .
RUN pip install --no-cache-dir -e .
RUN useradd -m -u 1000 lh && chown -R lh:lh /app
USER lh
EXPOSE 8002
CMD ["uvicorn", "leadharvester.server:app", "--host", "0.0.0.0", "--port", "8002"]
