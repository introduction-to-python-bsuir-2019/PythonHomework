from django import forms


class GetRSSForm(forms.Form):
    rss_source = forms.CharField(max_length=255)
