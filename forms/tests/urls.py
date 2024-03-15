from django.urls import path

from .views import *

app_name = 'tests'

urlpatterns = [
    path('<str:form_id>', form_view, name='form view'),
]