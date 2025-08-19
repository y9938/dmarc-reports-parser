#!/bin/bash

echo "🔄 Запуск parsedmarc..."

envsubst < "/etc/parsedmarc/parsedmarc.ini.template" > "/opt/parsedmarc/parsedmarc.ini"
parsedmarc -c /opt/parsedmarc/parsedmarc.ini

python3 /opt/parsedmarc/scripts/send_report.py

