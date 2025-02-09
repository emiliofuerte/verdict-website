# newsletter_site/newsletter_site/urls.py
from django.contrib import admin
from django.urls import include, path  # Make sure to import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletter.urls')),  # This pulls in the URLs defined in newsletter/urls.py
]