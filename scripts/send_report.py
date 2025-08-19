#!/usr/bin/env python3
import smtplib
import sys
import os
import json
import glob
from email.mime.text import MIMEText
from datetime import datetime
from email.utils import formatdate

def read_reports():
    body_parts = []
    json_files = glob.glob('/output/*.json')
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        body_parts.append(f"--- Файл: {filename} ---")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Форматируем данные как нужно
            body_parts.append(json.dumps(data, indent=2))
        body_parts.append("")  # Пустая строка между файлами
    
    return '\n'.join(body_parts)

def send_report():
    # Настройки email из переменных окружения
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    username = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    recipient = os.getenv('RECIPIENT_EMAIL')
    
    if not all([smtp_server, username, password, recipient]):
        print("❌ Не все email настройки установлены")
        sys.exit(1)
    
    try:
        # Формируем письмо
        subject = f"DMARC Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body = read_reports()
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = recipient
        msg['Date'] = formatdate(localtime=True)
        
        # Отправляем
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Отчет отправлен")
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_report()

