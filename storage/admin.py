from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from storage.models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = (
        "download_url",
        "author",
        "user",
        "uploaded_at",
        "is_public",
        "qr_code_preview",
        "download_qr_code",
    )
    list_filter = ("is_public", "uploaded_at")
    exclude = ("user",)
    search_fields = ("stored_file", "author", "user__username")
    ordering = ("-uploaded_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        """Allow users to change only their own files"""
        if request.user.is_superuser:
            return True
        return obj is None or obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        """Allow users to delete only their own files"""
        if request.user.is_superuser:
            return True
        return obj is None or obj.user == request.user

    def qr_code_preview(self, obj):
        """
        Displays a dynamically generated QR code as an image in the admin list view.
        """
        qr_code_base64 = obj.qr_code_base64()  # Dynamically generate the QR code
        return mark_safe(f'<img src="{qr_code_base64}" width="100" height="100" />')

    def save_model(self, request, obj, form, change):
        if not change or not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    qr_code_preview.short_description = "QR Code"

    def download_qr_code(self, obj):
        url = reverse("download_qr_code", args=[obj.pk])
        return mark_safe(f'<a href="{url}">Stáhnout QR kód</a>')

    download_qr_code.short_description = "Stáhnout QR kód"
