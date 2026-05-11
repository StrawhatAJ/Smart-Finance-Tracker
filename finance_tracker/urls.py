from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),     # enables /admin/
    path('', include('tracker.urls')),   # includes all tracker app URLs
]
