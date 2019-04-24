from .views import *
from django.urls import path

app_name='browser_app'
urlpatterns = [
    path('view/<str:path>', ContentView.as_view(), name='contentview'),
    path('view/np/<str:path>', NumpyView.as_view(), name='npview'),
    path('', Home.as_view(), name='home'),
]