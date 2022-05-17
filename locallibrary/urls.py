"""locallibrary URL Configuration

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

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from locallibrary import views as library_view

urlpatterns = [
     path('', library_view.home_page, name='home'),
     path('admin/', admin.site.urls),
     path('', RedirectView.as_view(url='', permanent=True)),
     path('accounts/', include('django.contrib.auth.urls')),
     path('catalog/', include('catalog.urls')),
]
STATIC_ROOT = "static/"
# use of static() to add URL maping to serve static files deuring development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Local Library main route
# root/home -> own views home view function
# root/catalog -> points to catalog route
# root empty -> Redirects to catalog/ -> '' view