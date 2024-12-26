# myapp/urls.py
from django.urls import path
from . import views  # Import your view functions

urlpatterns = [
    path('', views.index, name='index'),  # This maps the root URL to the 'index' view
]
