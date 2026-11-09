FROM python:3.12-slim
WORKDIR /app
COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt && useradd --uid 10001 --create-home appuser
COPY evidencepilot ./evidencepilot
RUN mkdir /data && chown appuser /data
USER appuser
ENV QUOTA_DB=/data/quota.sqlite3
EXPOSE 8000
# One process is required for the global concurrency lock. Persist /data.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--timeout", "300", "--access-logfile", "/dev/null", "evidencepilot.web:app"]
