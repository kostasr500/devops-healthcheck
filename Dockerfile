FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


#gia asfaleia to kanw na min trexei me root adeia
COPY src/ ./src/

RUN useradd -u 1000 -m appuser
USER appuser

# output help an den exoume dwsei website link
ENTRYPOINT ["python", "src/health_check.py"]
CMD ["--help"]
