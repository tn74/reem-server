from .views import *
from django.urls import path

app_name='browser_app'
urlpatterns = [
    path('retrieve/<str:log_folder>/<str:time_point>', Retrieval.as_view(), name='retrievalview'),
]