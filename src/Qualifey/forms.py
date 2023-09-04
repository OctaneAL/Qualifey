from django import forms
import json, os
from scraping.utils import get_all_keywords_keys

class FindForm(forms.Form):
    # language = forms.ModelChoiceField(
    #     queryset=['python', 'java', 'js', 'c++'],
    #     required=True,
    #     # widget=forms.Select(attrs={'class': 'form-control my-2'}),
    #     label='Специальность',
    # )

    # !!! GET FROM DB !!!
    CHOICES = (
        (i, i) for i in get_all_keywords_keys()
    )
    language = forms.MultipleChoiceField(
        choices = CHOICES,
        required = False,
        label = 'Спеціальність',
        widget=forms.Select,
    )