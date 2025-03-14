from django.contrib import admin
from storage.models import ActionType, Action

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
