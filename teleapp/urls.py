from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignupView.as_view(),name='SignUp'),
    path('login/', LoginView.as_view(), name='login'),
    path('mycontacts/',MyConatactListAPIView.as_view(),name='mycontacts'),
    path('spam/',ReportSpamAPIView.as_view(),name='report-spam'),
    path('all-spam-users/',GetAllSpamNumbersAPIView.as_view(),name='all-spam-users')
]