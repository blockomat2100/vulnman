from django import forms
from apps.networking import models
from vulnman.forms import NamedInlineFormSetFactory


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        exclude = ["uuid", "project", "creator"]


class HostnameInline(NamedInlineFormSetFactory):
    model = models.Hostname
    exclude = ["uuid", "host"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 4}
