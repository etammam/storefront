from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.say_hello),
    path('greeting/', views.greeting),
    path('greeting/<str:name>', views.greeting_someone)
]
