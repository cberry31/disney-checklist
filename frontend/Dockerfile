FROM alpine:latest

RUN apk add --no-cache \
    nodejs \
    npm \
    && npm install -g http-server

WORKDIR /app
COPY . .
EXPOSE 5500
CMD ["http-server", "-p", "5500", "-c-1"]
