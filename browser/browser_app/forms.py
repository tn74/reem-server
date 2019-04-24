from django import forms
from jsoneditor.fields.django_json_field import JSONField


class SearchForm(forms.Form):
    path = forms.CharField(label='Your name', max_length=100)
    json = JSONField()