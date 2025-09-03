from django.contrib import admin
from django.urls import path, include
from myapp.views import render_homepage  # You need to import the view from your app.

urlpatterns = [
    # This path handles the root URL of your website (e.g., http://127.0.0.1:8000/).
    path('', render_homepage, name='home'),
    
    # This path includes all URL patterns from your app.
    path('api/', include('myapp.urls')),

    # This path is for the built-in Django admin interface.
    path('admin/', admin.site.urls),
]
