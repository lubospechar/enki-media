from django.contrib import admin
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
    list_display = ("stored_file", "author", "user", "uploaded_at", "is_public")
    list_filter = ("is_public", "uploaded_at")
    search_fields = ("stored_file", "author", "user__username")
    ordering = ("-uploaded_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)