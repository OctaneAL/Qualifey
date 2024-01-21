from django import forms
import json, os
from scraping.utils import get_all_keywords_keys
from scraping.models import Skill, JobTitle, Country
from django_site.utils import is_migration

class FindForm(forms.Form):
    # language = forms.ModelChoiceField(
    #     queryset=['python', 'java', 'js', 'c++'],
    #     required=True,
    #     # widget=forms.Select(attrs={'class': 'form-control my-2'}),
    #     label='Специальность',
    # )

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

class ChartCountForm(forms.Form):
    JOB_TITLES = ()
    COUNTRIES = ()
    if not is_migration():
        JOB_TITLES = (
            sorted((i.name, i.name) for i in JobTitle.objects.all())
        )
        COUNTRIES = (
            # sorted((i.name, i.name) for i in Country.objects.all())
            sorted((name, name) for name in ['Germany', 'France', 'Ukraine'])
        )

    job_title = forms.MultipleChoiceField(
        choices = JOB_TITLES,
        required = True,
        label = 'Спеціальність',
        widget=forms.Select,
    )

    country = forms.MultipleChoiceField(
        choices = COUNTRIES,
        required = False,
        label = 'Країна',
        widget=forms.Select,
    )

class ChartIncreaseForm(forms.Form):
    JOB_TITLES = ()
    COUNTRIES = ()
    if not is_migration():
        JOB_TITLES = (
            sorted((i.name, i.name) for i in JobTitle.objects.all())
        )
        COUNTRIES = (
            # sorted((i.name, i.name) for i in Country.objects.all())
            sorted((name, name) for name in ['Germany', 'France'])
        )

    job_title = forms.MultipleChoiceField(
        choices = JOB_TITLES,
        required = True,
        label = 'Спеціальність',
        widget=forms.Select,
    )

    country = forms.MultipleChoiceField(
        choices = COUNTRIES,
        required = False,
        label = 'Країна',
        widget=forms.Select,
    )
