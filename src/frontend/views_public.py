
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'public/index.html'


index = IndexView.as_view()
