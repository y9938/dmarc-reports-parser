# Build stage
FROM python:3.9-slim AS builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libxml2-dev \
    libxslt-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U parsedmarc

# Runtime stage  
FROM python:3.9-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# (gettext) for envsubst

RUN useradd -r -s /bin/false -m -d /opt/parsedmarc parsedmarc

RUN mkdir -p /output /etc/parsedmarc/ /opt/parsedmarc/scripts \
    && chown -R parsedmarc:parsedmarc /opt/parsedmarc /output

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

USER parsedmarc
WORKDIR /opt/parsedmarc
CMD ["/opt/parsedmarc/scripts/run_parser.sh"]

