from django import forms
import json, os

def get_all_keywords_keys(path: str = os.path.join(os.getcwd(), 'scraping', 'data', 'keywords.json')) -> list[str]:
    data = read_json(path)

    return list(data.keys())

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

class FindForm(forms.Form):
    # language = forms.ModelChoiceField(
    #     queryset=['python', 'java', 'js', 'c++'],
    #     required=True,
    #     # widget=forms.Select(attrs={'class': 'form-control my-2'}),
    #     label='Специальность',
    # )
    CHOICES = (
        (i, i) for i in get_all_keywords_keys()
    )
    language = forms.MultipleChoiceField(
        choices = CHOICES,
        required = False,
        label = 'Спеціальність',
        widget=forms.Select,
    )