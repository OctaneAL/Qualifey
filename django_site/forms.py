from django import forms
import json, os
from scraping.utils import get_all_keywords_keys
from scraping.models import Skill
from django_site.utils import is_migration

class FindForm(forms.Form):
    # language = forms.ModelChoiceField(
    #     queryset=['python', 'java', 'js', 'c++'],
    #     required=True,
    #     # widget=forms.Select(attrs={'class': 'form-control my-2'}),
    #     label='Специальность',
    # )

    # !!! GET FROM DB !!!
    if not is_migration():
        CHOICES = (
            sorted((i.skill, i.skill) for i in Skill.objects.all())
        )
    else:
        CHOICES = ()
    language = forms.MultipleChoiceField(
        choices = CHOICES,
        required = False,
        label = 'Спеціальність',
        widget=forms.Select,
    )