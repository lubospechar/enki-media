from django.http import HttpResponse, Http404
from django.views.generic.detail import DetailView
from .models import UploadedFile


class PublicFileView(DetailView):
    model = UploadedFile
    context_object_name = "uploaded_file"

    def get(self, request, *args, **kwargs):
        # Try to fetch the object; raises Http404 if not found or not public
        obj = self.get_object()

        if not obj.is_public:
            raise Http404("This file is not public.")

        # Opens the file for download
        response = HttpResponse(obj.stored_file.open("rb"), content_type="application/octet-stream")

        # Sets the HTTP headers for file download
        response["Content-Disposition"] = f'attachment; filename="{obj.stored_file.name.split("/")[-1]}"'
        return response
