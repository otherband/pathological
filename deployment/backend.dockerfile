FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && apt install curl -y
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ ./backend/
COPY deployment/run_backend.sh run_backend.sh
RUN pip install ./backend/