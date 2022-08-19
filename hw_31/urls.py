"""hw_28 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


from django.urls import path, include
from rest_framework import routers

from ads.views import CategoryViewSet
from users.views import LocationViewSet

location_router = routers.SimpleRouter()
location_router.register('location', LocationViewSet)

category_router = routers.SimpleRouter()
category_router.register('category', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ad/', include('ads.ad_urls')),
    path('selection/',   include('ads.selection_urls')),
    path('user/', include('users.urls')),
]

urlpatterns += location_router.urls
urlpatterns += category_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
