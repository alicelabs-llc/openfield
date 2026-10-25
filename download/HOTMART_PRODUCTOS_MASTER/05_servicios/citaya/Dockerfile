FROM python:3.12-slim
LABEL maintainer="Eddy Flores"
LABEL org.opencontainers.image.title="CitaYa"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e .
RUN useradd -m -u 1000 citaya && chown -R citaya:citaya /app
USER citaya
EXPOSE 8005
CMD ["uvicorn", "citaya.server:app", "--host", "0.0.0.0", "--port", "8005"]
