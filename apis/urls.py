from apis import views
from django.urls import path

urlpatterns = [
    path('getresponse', views.get_response, name='get_response'),
]