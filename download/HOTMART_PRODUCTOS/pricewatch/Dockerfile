FROM python:3.12-slim
LABEL maintainer="Eddy Flores"
LABEL org.opencontainers.image.title="PriceWatch"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e .
RUN useradd -m -u 1000 pw && chown -R pw:pw /app
USER pw
EXPOSE 8003
CMD ["uvicorn", "pricewatch.server:app", "--host", "0.0.0.0", "--port", "8003"]
