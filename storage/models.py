import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
import base64
from django.core.files.base import ContentFile


# Represents a stored_file uploaded by a user
class UploadedFile(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID"
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Uživatel",
        help_text="Uživatel, který soubor nahrál.",
    )
    author = models.CharField(
        max_length=255, verbose_name="Autor", help_text="Autor souboru."
    )
    stored_file = models.FileField(
        upload_to="uploads/%Y/%m/", verbose_name="Soubor", help_text="Nahraný soubor."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Datum nahrání",
        help_text="Datum a čas, kdy byl soubor nahrán.",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Veřejný přístup",
        help_text="Určuje, zda je soubor veřejně dostupný.",
    )

    class Meta:
        verbose_name = "Nahraný soubor"
        verbose_name_plural = "Nahrané soubory"

    def __str__(self):
        return f"{self.stored_file.name} ({self.author})"

    def download_url(self):
        return f"{settings.DOWNLOAD_URL}{self.id}"

    def qr_code_base64(self):
        """
        Generates a QR code dynamically as a Base64-encoded image.
        """
        # Generate the QR code data from the download URL
        url = self.download_url()

        # Create a QR code object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create the QR code image
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image into a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encode the image as Base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_base64}"

    def qr_code_data(self):
        return reverse("download_qr_code", args=[self.pk])
