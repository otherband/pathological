FROM node:22-bookworm-slim as builder


WORKDIR /build

RUN apt-get update && apt install default-jre -y
COPY open-api/ ./open-api/
RUN cd open-api && npm install && npm run generate-typescript

WORKDIR /build/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build


FROM nginx:1.25.2-alpine

COPY --from=builder /build/frontend/dist/ /usr/share/nginx/html/
