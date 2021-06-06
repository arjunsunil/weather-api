

import pandas as pd
import os
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.core.validators import validate_email
from . import serializers
from . import utils


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EXCEL_PATH = os.path.abspath(os.path.join(BASE_DIR, 'excel.xlsx'))



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1

    
class UserListView(generics.ListAPIView):
    """ User list view """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ListWeather(APIView):
    """ Weather list view """

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        """ List the weather infomation of 30 cities"""
        try:
            return Response(utils.get_weather_data())
        except Exception as e :
            return APIException(str(e))


class SendEmail(APIView):
    """ To send the weather information to a list of emails"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            self.send_weather_mail(request)
        except Exception as e :
            return APIException(str(e))
        return Response("Emails send sucessfully")

    def send_weather_mail(self, request):
        """send excel weather report to valid emails"""

        weather_data = []
        emails = request.data.get("emails")
        valid_emails = self.get_vali_emails(emails)
        weather_data = utils.get_valid_emails()
        df = pd.DataFrame(weather_data)
        df.to_excel(EXCEL_PATH)
        data = open(EXCEL_PATH, 'rb').read()
        try:
            mail = EmailMessage("Weather Report", "Weather Report", 'weathertestarjun@gmail.com', valid_emails)
            mail.attach('file.xlsx', data)
            mail.send()
        except:
            pass

    def get_valid_emails(self, emails):
        """ validate the input emails"""
        valid_emails = []
        for email in emails:
            try:
                validate_email(email)
            except:
                pass
            else:
                valid_emails.append(email)
        return valid_emails