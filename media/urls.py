from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from storage.views import PublicFileView, QRCodeDownloadView

urlpatterns = [
    path('files/<uuid:pk>/', PublicFileView.as_view(), name='public_file'),
    path('<uuid:pk>/download_qr_code/', QRCodeDownloadView.as_view(), name='download_qr_code'),
    path("", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
