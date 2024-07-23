FROM node:22-bookworm-slim as open-api-builder


WORKDIR /build/open-api

RUN apt-get update && apt install default-jre -y
COPY open-api/ ./
RUN npm install && npm run generate-python

FROM python:3.9-slim-buster
WORKDIR /app

RUN apt-get update && apt install curl -y
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

WORKDIR /app/generated
COPY --from=open-api-builder /build/open-api/generated/ ./
RUN cd pathological-python-api && pip install .

WORKDIR /app
COPY backend/ ./backend/
COPY deployment/run_backend.sh run_backend.sh
RUN pip install ./backend/