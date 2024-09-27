from django.contrib import admin
from django.urls import path, include
from chat.views import index  # Import the index view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('', index),  # Add this line to handle the root URL
]
