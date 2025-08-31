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
    has_failures = False
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        
        if not data:
            continue

        reports = data if isinstance(data, list) else [data]
        
        for rep in reports:
            records = rep.get("records", [])
            for rec in records:
                align = rec.get("alignment", {})
                if not all(align.get(x, False) for x in ("spf", "dkim", "dmarc")):
                    has_failures = True
                    body_parts.append(f"--- Файл: {filename} (обнаружены проблемы) ---")
                    body_parts.append(json.dumps(data, indent=2, ensure_ascii=False))
                    body_parts.append("")
                    # достаточно один раз добавить файл
                    break
            if has_failures:
                break
    
    return '\n'.join(body_parts), has_failures

def send_report():
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    username = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    recipient = os.getenv('RECIPIENT_EMAIL')
    
    if not all([smtp_server, username, password, recipient]):
        print("❌ Не все email настройки установлены")
        sys.exit(1)
    
    try:
        subject = f"DMARC Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body, has_failures = read_reports()

        if not has_failures:
            print("✅ Все выравнивания SPF/DKIM/DMARC в порядке — письмо не отправлено")
            return
        
        msg = MIMEText(body, _charset="utf-8")
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
        
        print("✅ Отчет отправлен (есть проблемные записи)")
         
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_report()

