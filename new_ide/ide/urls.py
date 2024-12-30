from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('run_code/', views.run_code, name = 'run_code')
]