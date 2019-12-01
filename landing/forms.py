from django import forms


class MainForm(forms.Form):
     rss = forms.CharField(max_length=300)
     limit = forms.IntegerField()