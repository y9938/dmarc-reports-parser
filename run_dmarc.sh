#!/bin/bash

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --rm \
  -v "$BASE_DIR/config:/etc/parsedmarc" \
  -v "$BASE_DIR/scripts:/opt/parsedmarc/scripts" \
  --env-file "$BASE_DIR/.env" \
  dmarc-reports-parser:latest

