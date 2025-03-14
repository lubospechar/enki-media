from django.db import models

# Represents a type of action
class ActionType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Název typu",
        help_text="Unikátní název typu akce."
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
        help_text="Vyberte typ akce."
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Název akce",
        help_text="Zadejte název akce."
    )

    class Meta:
        verbose_name = "Akce"
        verbose_name_plural = "Akce"

    def __str__(self):
        return f"{self.type}: {self.name}"
