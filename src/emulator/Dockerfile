FROM python:3.11-slim

# Criação de usuário não-privilegiado
RUN groupadd -g 1000 emulatoruser && \
    useradd -u 1000 -g emulatoruser -s /bin/bash -m emulatoruser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN chown -R emulatoruser:emulatoruser /app
USER emulatoruser

CMD ["python", "-u", "main.py"]
