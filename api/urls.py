from .views import SendEmail, UserListView, ListWeather
from django.urls import path, include

urlpatterns = [
    path('weather/list/', ListWeather.as_view(), name='login'),
    path('users/', UserListView.as_view()),
    path('send/email/', SendEmail.as_view(), name='login'),
    path('auth/', include('rest_auth.urls'))
]
