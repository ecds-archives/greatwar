from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from xml.sax.saxutils import escape, unescape

class SimpleSearchForm(forms.Form):
    term  = forms.CharField(max_length=50, required=True)

    def clean_term(self):
        return self.escapeXml(self.cleaned_data['term'])

    def pretty_print_query(self):
        if self.cleaned_data['term'] == '':
            return ""
        else:
            return "Document contains \"%(pretty_term)s\"" % \
                {'pretty_term': self.unescapeXml(self.cleaned_data['term'])}

    def escapeXml(self, str):
        #saxutils.escape < > and & are handled by saxutils.escape
        return escape(str, {"'":"&apos;", '"':"&quot;"})

    def unescapeXml(self, str):
        #saxutils.unescape < > and & are handled by saxutils.unescape
        return unescape(str, {"&apos;": "'", "&quot;": '"'})


class BasicSearchBox(SimpleSearchForm):
	#term  				= forms.CharField(max_length=50, required=True)
	search_poetry 		= forms.BooleanField(required=False,initial=True,label="Poetry")
	search_postcards 	= forms.BooleanField(required=False,initial=False,label="Postcards")
	search_links 		= forms.BooleanField(required=False,initial=False,label="Links")
	
	def clean(self):
		cleaned_data = self.cleaned_data
		term = cleaned_data.get("term")
		search_poetry = cleaned_data.get("search_poetry")
		search_postcards = cleaned_data.get("search_postcards")
		search_links = cleaned_data.get("search_links")
		
		if not term:
			raise forms.ValidationError("Search term is not valid.")
		else:
			if not(search_poetry or search_postcards or search_links):
				raise forms.ValidationError("Please choose at least one search filed.")
			elif (search_postcards or search_links):
				raise forms.ValidationError("We can only search in poetry at this moment.")
		return cleaned_data

class AdvancedSearchBox(SimpleSearchForm):
	term  	= forms.CharField(max_length=50, required=False,label="Keyword")
	title	= forms.CharField(max_length=50, required=False,label="Title")
	author	= forms.CharField(max_length=50, required=False,label="Author")
	date	= forms.CharField(max_length=4, min_length=4,required=False,label="Date")
	
	def clean(self):
		cleaned_data = self.cleaned_data
		term = cleaned_data.get("term")
		title = cleaned_data.get("title")
		author = cleaned_data.get("author")
		date = cleaned_data.get("date")
		
		if not(term or title or author or date):
			raise forms.ValidationError("No search criterion.")
		return cleaned_data
		
		
class BasicSearchForm(SimpleSearchForm):
    #used to populate field select box on form.  Changes to option values must
    #result in corresponding changes to xQry output
    FIELD_CHOICES = (('title', 'Title + Study No.'),
                     ('abstract', 'Abstract'),
                     ('pi', 'Principal Investigator'),
                     ('subject', 'Subject Terms'),
                     ('geoCover', 'Geographic Coverage'),
                     ('timePrd', 'Time Coverage'),
                     ('entireDoc', 'All Fields'),)

    FIELD_STRINGS = {'title': 'Title or Study No:',
                     'abstract': 'Abstract:',
                     'pi': 'Principal Investigator:',
                     'subject': 'Subject:',
                     'geoCover': 'Geographic Coverage:',
                     'timePrd': 'Time Period:',
                     'entireDoc': 'All Fields:'}

    #form fields
    term  = forms.CharField(max_length=100, required=False)
    field = forms.CharField(widget=forms.Select(choices=FIELD_CHOICES))

	#ensure that form input exists in FIELD_CHOICES
    def clean_field(self):
        data = self.cleaned_data['field']
        if data == "":
            data = "entireDoc"
        keys = [ i[0] for i in self.FIELD_CHOICES ]
        if data not in keys:
            raise forms.ValidationError("Search field is not valid")

        return data

    def pretty_print_query(self):
        if self.cleaned_data['term'] == '':
            return ""
        else:
            return "%(pretty_qry)s %(pretty_term)s" % \
                {'pretty_qry': self.FIELD_STRINGS[self.cleaned_data['field']], \
                 'pretty_term': self.unescapeXml(self.cleaned_data['term'])}


class ExtendedSearchForm(forms.Form):
    operator = forms.CharField(
        widget=forms.RadioSelect(
            choices=(('and', 'Match All'), ('or', 'Match Any'))
        )
    )

    def clean_operator(self):
        return " %s " % (self.cleaned_data['operator'], )

    def pretty_print_query(self, form_list):
        pretty_print = []

        if self.cleaned_data.get('operator', 'and').strip() == 'and':
            pretty_print.append("All fields match:")
        else:
            pretty_print.append("Any fields match:")

        for f in form_list:
            if f.pretty_print_query():
                pretty_print.append(f.pretty_print_query())

        return "<br/>".join(pretty_print)

    def contains_form_data(self):
        #is bound does not verify that bound data exists on the form
        #only that any data has been bound
        for key in self.fields.keys():
            if key in self.data:
                return True
        return False

#Form Sets
class BaseSearchFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        failed = True
        for f in self.forms:            
            #formset must contain at least 1 valid term/field pair
            if (f.cleaned_data['term'] != ''):
                failed = False

        if failed:
            raise forms.ValidationError("Please specify at least one search term")

SearchFormSet = formset_factory(BasicSearchForm, extra=4, formset=BaseSearchFormSet)

