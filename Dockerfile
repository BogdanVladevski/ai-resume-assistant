#builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
  && pip install --prefix=/install --no-cache-dir -r requirements.txt


#runtime
FROM python:3.12-slim AS runtime

RUN useradd --create-home appuser
WORKDIR /home/appuser/app

COPY --from=builder /install /usr/local

COPY app/ ./app/

RUN chown -R appuser:appuser /home/appuser
USER appuser

EXPOSE 8000

#health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
