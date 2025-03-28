from django.http import HttpResponse, Http404
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

        response = HttpResponse(file.open("rb"), content_type="application/octet-stream")

        # Fallback filename (ASCII only), and UTF-8 encoded filename
        ascii_filename = file_name.encode("ascii", "ignore").decode()
        utf8_filename = quote(file_name)

        response["Content-Disposition"] = (
            f'attachment; filename="{ascii_filename}"; filename*=UTF-8\'\'{utf8_filename}'
        )

        return response
