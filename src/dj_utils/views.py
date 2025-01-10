import unicodedata

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse


class LoginAndPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass


class PDFResponseMixin(WeasyTemplateResponseMixin):

    class UTF8PdfTemplateResponse(WeasyTemplateResponse):
        def __init__(self, filename=None, *args, **kwargs):
            kwargs['content_type'] = "application/pdf"
            super().__init__(*args, **kwargs)
            if filename:
                try:
                    _filename = filename.encode('utf-8')
                except UnicodeEncodeError:
                    filenames = {
                        'filename': unicodedata.normalize('NFKD', filename).encode('utf-8', 'ignore'),
                        'filename*': "UTF-8''{}".format(filename),
                    }
                else:
                    filenames = {'filename': _filename, 'filename*': "UTF-8''{}".format(filename)}
                self['Content-Disposition'] = 'attachment; {}'.format("; ".join(["{}={}".format(k, v) for k, v in filenames.items()]))
            else:
                self['Content-Disposition'] = 'attachment'

    response_class = UTF8PdfTemplateResponse
