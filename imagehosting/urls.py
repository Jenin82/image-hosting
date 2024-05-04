from .views import image_to_url
from django.urls import path
urlpatterns = [
   
    path('imagetourl/',image_to_url,name='image_to_url'),
    
]