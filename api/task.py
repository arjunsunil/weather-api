from __future__ import absolute_import, unicode_literals

import os
import pandas as pd
from celery import shared_task
from django.core.mail import EmailMessage
from weather import settings



BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EXCEL_PATH = os.path.abspath(os.path.join(BASE_DIR, 'excel.xlsx'))

@shared_task
def send_weather_mail(valid_emails, weather_data):
    df = pd.DataFrame(weather_data)
    df.to_excel(EXCEL_PATH)
    data = open(EXCEL_PATH, 'rb').read()
    mail = EmailMessage("Weather Report", "Weather Report", settings.EMAIL_HOST_USER, valid_emails)
    mail.attach('file.xlsx', data)
    mail.send()