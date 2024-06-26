"""
URL configuration for marmut project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/auth/', permanent=False)),
    path('', include('album_song_royalti.urls')),
    path('', include('kelola_playlist.urls')),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('kelola_podcast.urls')),
    path('', include('melihat_chart.urls')),
    path('', include('play_podcast.urls')),
    path('paket/', include('paket.urls')),
    path('', include('play_song.urls')),
]
