from django import forms


class CertForm(forms.Form):
    host = forms.CharField(label='Host', required=False)
    server = forms.CharField(label='Server',
                             help_text='Optional, in case you want to download certificate from a '
                                       'different origin server than what the DNS refers to',
                             required=False)
    cert = forms.FileField(label='Certificate File', required=False)
    body = forms.CharField(label='Certificate', required=False, widget=forms.Textarea(attrs={'rows': 15}))

    def clean(self):
        if not (self.cleaned_data['host'] or self.cleaned_data['cert'] or self.cleaned_data['body']):
            raise forms.ValidationError('Please fill in one of the forms')
        return self.cleaned_data
