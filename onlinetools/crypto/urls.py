""""online-tools crypto URLs"""

from django.urls import path

from .views import CertView


app_name = 'crypto'
urlpatterns = [
    path('cert', CertView.as_view(), name='cert'),
]
