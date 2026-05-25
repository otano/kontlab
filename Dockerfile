FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gestion_asso/ .

EXPOSE 8000

CMD ["gunicorn", "gestion_asso.wsgi:application", "--bind", "0.0.0.0:8000"]
