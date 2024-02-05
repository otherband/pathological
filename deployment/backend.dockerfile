FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
RUN pip install ./backend/
ENTRYPOINT ["cd", "src/pathological/", "&&", "python3", "app.py"]