FROM python:3.13-slim

WORKDIR /app

RUN useradd -m dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=dev:dev . .

EXPOSE 3000
USER dev

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "dash_api:app"]