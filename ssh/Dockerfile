FROM python:3.13-slim

RUN useradd -m -d /app app && \
    chown -R app:app /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

EXPOSE  2222

USER app

CMD ["python", "ssh.py"]
