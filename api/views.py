

import os

from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from django.core.validators import validate_email
from . import serializers
from . import utils
from api.task import send_weather_mail

    
class UserListView(generics.ListAPIView):
    """ User list view """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ListWeather(APIView):
    """ Weather list view """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """ List the weather infomation of 30 cities"""

        try:
            # Django rest pagination implement using limit and offset
            offset = int(self.request.query_params.get('offset', 0))
            limit = int(self.request.query_params.get('limit', offset + 10))
            return Response(utils.get_weather_data(offset,  limit))
        except Exception as e :
            return APIException(str(e))


class SendEmail(APIView):
    """ To send the weather information to a list of emails"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """send excel weather report to valid emails"""

        emails = request.data.get("emails")
        valid_emails = self.get_valid_emails(emails)
        weather_data = utils.get_weather_data()
        send_weather_mail.delay(valid_emails, weather_data)

        return Response("Emails send sucessfully")
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