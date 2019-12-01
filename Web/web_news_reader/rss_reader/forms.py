from django import forms
from django.core.exceptions import ValidationError

import feedparser

FORMATS = (
    (1, ("Read on website")),
    (2, ("Save as json")),
    (3, ("Save as .fb2")),
    (4, ("Save as .pdf")),
)

FORMATS_DICT = {}

for format_ in FORMATS:
    FORMATS_DICT[format_[0]] = format_[1]


class SettingsForm(forms.Form):
    link = forms.CharField(max_length=100)
    limit = forms.CharField(max_length=5)
    format_ = forms.ChoiceField(choices=FORMATS)

    link.widget.attrs.update({'class': 'form-control'})
    limit.widget.attrs.update({'class': 'form-control', 'value': 0})

    def clean_limit(self):
        new_limit = self.cleaned_data['limit']

        if new_limit.isdigit():
            return new_limit
        raise ValidationError('Limit is must be integer!')

    def clean_link(self):
        new_link = self.cleaned_data['link']

        try:
            rss = feedparser.parse(new_link)
            rss.feed.title
        except AttributeError:
            raise ValidationError('Incorrect link')

        return new_link
