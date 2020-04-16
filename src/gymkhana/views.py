from shutil import rmtree
from tarfile import open as tar_open
from os.path import join
from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView


class UploadForm(forms.Form):
    file = forms.FileField()

    def process(self):
        # Delete directory if present, then extract new archive
        rmtree(join(settings.VUE_ROOT, 'dist'), ignore_errors=True)
        with tar_open(fileobj=self.cleaned_data['file'].file, mode='r:gz') as archive:
            archive.extractall(settings.VUE_ROOT)
            archive.close()

    def clean_file(self):
        if not self.cleaned_data['file'].content_type == 'application/gzip':
            raise ValidationError("Not a valid file")
        return self.cleaned_data['file']


class FrontendUpdateView(FormView):
    form_class = UploadForm
    template_name = 'frontend_update.html'
    success_url = reverse_lazy('admin:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Frontend Upload',
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
            'site_url': admin.site.site_url,
            'has_permission': admin.site.has_permission(self.request),
            'is_popup': False,
        })
        return context

    def form_valid(self, form):
        form.process()
        messages.add_message(self.request, messages.INFO, 'The frontend code deployment has started')
        return super().form_valid(form)
