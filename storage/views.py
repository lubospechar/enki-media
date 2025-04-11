from io import BytesIO

import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from .models import UploadedFile
from urllib.parse import quote


class PublicFileView(DetailView):
    model = UploadedFile
    context_object_name = "uploaded_file"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if not obj.is_public:
            raise Http404("This file is not public.")

        file = obj.stored_file
        file_name = file.name.split("/")[-1]

        response = HttpResponse(
            file.open("rb"), content_type="application/octet-stream"
        )

        # Fallback filename (ASCII only), and UTF-8 encoded filename
        ascii_filename = file_name.encode("ascii", "ignore").decode()
        utf8_filename = quote(file_name)

        response["Content-Disposition"] = (
            f"attachment; filename=\"{ascii_filename}\"; filename*=UTF-8''{utf8_filename}"
        )

        return response


class QRCodeDownloadView(LoginRequiredMixin, View):
    """
    Class-Based View pro stažení QR kódu ve vysokém rozlišení.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            uploaded_file = UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            raise Http404("Objekt Nahraný soubor neexistuje nebo byl odstraněn.")

        qr_data = reverse("download_qr_code", args=[uploaded_file.pk])

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((900, 900))

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="image/png")
        response["Content-Disposition"] = (
            f'attachment; filename="{uploaded_file.pk}_qr_code.png"'
        )
        return response
