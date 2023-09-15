from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('table_list/', views.table_list, name='table_list'),
]
