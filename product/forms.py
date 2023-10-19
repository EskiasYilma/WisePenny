from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(widget=forms.TextInput(
        attrs={'class': "search_main col-xs-10", 'placeholder': "iPhone 14, Epson Printer, LG tv...", 'id':"searchBar", 'type': "text", 'aria-label': "Search for a Product here", 'aria-describedby': "basic-addon2", "font-size": "10px"}), required=True)
class UrlShortnerForm(forms.Form):
    url_text = forms.URLField(widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Paste Long URL Here (https://...)", 'type': "url", 'aria-label': "Paste Long URL Here", 'aria-describedby': "basic-addon2", "font-size": "10px"}), required=True)
class SubscribeForm(forms.Form):
    sub_form = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Email Address...", 'type': "email", 'aria-label': "Email Address ...", 'aria-describedby': "basic-addon2", "font-size": "10px"}), required=True)
class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Name", 'type': "text", 'aria-label': "full_name", 'aria-describedby': "basic-addon2", "font-size": "12px"}), required=True)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Email Address", 'type': "email", 'aria-label': "email", 'aria-describedby': "basic-addon2", "font-size": "12px"}), required=True)
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Mobile Number", 'type': "tel", 'aria-label': "phone", 'aria-describedby': "basic-addon2", "font-size": "12px"}), required=False)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'placeholder': "Message", 'type': "text", 'aria-label': "message", 'aria-describedby': "basic-addon2", "font-size": "15px", 'rows': 10, 'cols': 15}), required=True)
