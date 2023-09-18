from django.urls import path
from . import views

urlpatterns = [
    path('worker/', views.worker_view, name='worker'),
    path('tested/', views.tested_view, name= 'tested'),
    path('conttest/', views.contats_view, name = 'conttest')
    # Додайте інші URL-шляхи за потреби
]
