"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

import os
import re
from django.http import FileResponse, HttpResponse, Http404
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

def stream_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1

            length = end - start + 1

            f = open(file_path, "rb")
            f.seek(start)

            response = HttpResponse(
                f.read(length),
                status=206,
                content_type="video/mp4"
            )

            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            response["Accept-Ranges"] = "bytes"
            response["Content-Length"] = str(length)
            return response

    response = FileResponse(open(file_path, "rb"), content_type="video/mp4")
    response["Content-Length"] = str(file_size)
    response["Accept-Ranges"] = "bytes"
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    re_path(r"^media/(?P<path>.*)$", stream_media),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)