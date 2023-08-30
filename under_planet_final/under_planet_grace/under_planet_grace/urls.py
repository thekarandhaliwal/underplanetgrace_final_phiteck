"""
URL configuration for under_planet_grace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from planet import views
from planet.views import convert_html_to_pdf, convert, UnderPlanetGrace
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', convert, name='index1'),
    path('under-planet-grace/',  views.UnderPlanetGrace.as_view(), name='under-planet-grace'),
    path('convert_html_to_pdf', convert_html_to_pdf, name='convert_html_to_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

