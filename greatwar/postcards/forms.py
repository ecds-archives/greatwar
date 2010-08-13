from django import forms

class SearchForm(forms.Form):
    #keyword = forms.CharField(help_text='Search anywhere in postcard metadata')
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
