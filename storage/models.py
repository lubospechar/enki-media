import uuid

from django.db import models
from django.contrib.auth import get_user_model

# Represents a type of action
class ActionType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Název typu",
        help_text="Unikátní název typu akce.",
    )

    class Meta:
        verbose_name = "Typ akce"
        verbose_name_plural = "Typy akcí"

    def __str__(self):
        return self.name


# Represents an action linked to a specific type
class Action(models.Model):
    type = models.ForeignKey(
        ActionType,
        on_delete=models.CASCADE,
        verbose_name="Typ akce",
        help_text="Vyberte typ akce.",
    )
    name = models.CharField(
        max_length=255, verbose_name="Název akce", help_text="Zadejte název akce."
    )

    class Meta:
        verbose_name = "Akce"
        verbose_name_plural = "Akce"

    def __str__(self):
        return f"{self.type}: {self.name}"

# Represents a stored_file uploaded by a user
class UploadedFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID"
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Uživatel",
        help_text="Uživatel, který soubor nahrál."
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Autor",
        help_text="Autor souboru."
    )
    stored_file = models.FileField(
        upload_to="uploads/%Y/%m/",
        verbose_name="Soubor",
        help_text="Nahraný soubor."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Datum nahrání",
        help_text="Datum a čas, kdy byl soubor nahrán."
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Veřejný přístup",
        help_text="Určuje, zda je soubor veřejně dostupný."
    )

    class Meta:
        verbose_name = "Nahraný soubor"
        verbose_name_plural = "Nahrané soubory"

    def __str__(self):
        return f"{self.stored_file.name} ({self.author})"
