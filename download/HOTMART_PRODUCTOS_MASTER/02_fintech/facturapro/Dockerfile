FROM python:3.12-slim
LABEL maintainer="Eddy Flores <eddyflores100@gmail.com>"
LABEL org.opencontainers.image.title="FacturaPro"
LABEL org.opencontainers.image.description="Facturación electrónica SRI + CFDI 4.0 self-hosted"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e .
RUN useradd -m -u 1000 facturapro && chown -R facturapro:facturapro /app
USER facturapro
EXPOSE 8001
CMD ["uvicorn", "facturapro.server:app", "--host", "0.0.0.0", "--port", "8001"]
