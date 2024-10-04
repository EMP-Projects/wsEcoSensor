# Usa un'immagine base di Python
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa virtualenv
RUN pip install virtualenv

# Crea un ambiente virtuale
RUN virtualenv venv

# Attiva l'ambiente virtuale e installa le dipendenze
RUN . venv/bin/activate && pip install -r requirements.txt

# Copia il resto del codice dell'applicazione nella directory di lavoro
COPY . .

# Espone la porta su cui l'applicazione sarà in ascolto
EXPOSE 8000

# Comando per avviare l'applicazione
CMD ["sh", "-c", ". venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"]