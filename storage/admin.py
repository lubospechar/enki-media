from django.contrib import admin
from django.utils.safestring import mark_safe

from storage.models import ActionType, Action, UploadedFile

@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name", "type__name")
    ordering = ("name",)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("id", "stored_file", "author", "user", "uploaded_at", "is_public", 'qr_code_preview')
    list_filter = ("is_public", "uploaded_at")
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

    qr_code_preview.short_description = "QR Code"
