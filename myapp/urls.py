from django.urls import path
from myapp import views as vw

urlpatterns = [
    path('',vw.Home.as_view(),name='home'),
]