from django.urls import path
from . import views

app_name = 'blog2'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<str:title>/', views.post_detail, name='post_detail'),
]