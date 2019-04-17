from django import forms


class SearchForm(forms.Form):
    path = forms.CharField(label='Your name', max_length=100)