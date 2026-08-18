FROM python:3.13-slim

WORKDIR /app

RUN useradd dev 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=dev:dev . .

EXPOSE 5000

USER dev 

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "honey_pot:app"]