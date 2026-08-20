FROM python:3.13-slim


RUN useradd -m -d /app app && \
    chown -R app:app /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

EXPOSE 5000

USER app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "honey_pot:app"]