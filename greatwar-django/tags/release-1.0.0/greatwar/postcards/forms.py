from django import forms

class SearchForm(forms.Form):
    #keyword = forms.CharField(help_text='Search anywhere in postcard metadata')
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def clean(self):
        """Custom form validation."""
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        #Validate at least one term has been entered
        if not title and not description:
            del cleaned_data['title']
            del cleaned_data['description']

            raise forms.ValidationError("Please enter search terms for title or description")

        return cleaned_data
