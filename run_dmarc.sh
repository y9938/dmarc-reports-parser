#!/bin/bash

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$(docker images -q dmarc-reports-parser:latest)" ]; then
  echo "Не найден образ, билдим…"
  docker build -t dmarc-reports-parser:latest "$BASE_DIR"
fi

docker run --rm \
  -v "$BASE_DIR/config:/etc/parsedmarc" \
  -v "$BASE_DIR/scripts:/opt/parsedmarc/scripts" \
  --env-file "$BASE_DIR/.env" \
  dmarc-reports-parser:latest
