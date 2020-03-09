from django import forms


class CertForm(forms.Form):
    cert = forms.FileField(label='Certificate File', required=False)
    body = forms.CharField(label='Certificate', required=False, widget=forms.Textarea(attrs={'rows': 15}))
