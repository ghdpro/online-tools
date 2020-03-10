from django.urls import reverse
from django.views.generic import FormView

from .forms import CertForm
from .logic import get_certificate_from_host, parse_certificate


class CertView(FormView):
    form_class = CertForm
    template_name = 'crypto/cert.html'

    def form_valid(self, form):
        cert = None
        context = self.get_context_data()
        if form.cleaned_data['host']:
            try:
                server = form.cleaned_data['server'] if form.cleaned_data['server'] else None
                cert = get_certificate_from_host(form.cleaned_data['host'], server)
                context['tab'] = 'host'
            except Exception as e:
                context['error'] = 'Unable to download certificate from host'
        elif form.cleaned_data['cert']:
            cert = form.cleaned_data['cert'].read()
            context['tab'] = 'upload'
        elif form.cleaned_data['body']:
            cert = form.cleaned_data['body']
            context['tab'] = 'text'
        try:
            if cert is not None:
                context['x509'] = parse_certificate(cert)
        except Exception as e:
            context['error'] = 'Unable to parse certificate'
        return self.render_to_response(context)
