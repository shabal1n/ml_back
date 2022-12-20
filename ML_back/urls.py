"""ML_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.http import StreamingHttpResponse
from django.urls import path

from app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app.views import gen, VideoCamera

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.main),
                  path('upload', views.upload_display_video, name='upload_display_video'),
                  path('live', lambda r: StreamingHttpResponse(gen(VideoCamera()),
                                                               content_type='multipart/x-mixed-replace; boundary=frame'),
                       name='live'),
              ] + staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
