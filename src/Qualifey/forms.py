from django import forms

class FindForm(forms.Form):
    # language = forms.ModelChoiceField(
    #     queryset=['python', 'java', 'js', 'c++'],
    #     required=True,
    #     # widget=forms.Select(attrs={'class': 'form-control my-2'}),
    #     label='Специальность',
    # )
    CHOICES = (
        ('python', 'Python'),
        ('java', 'Java'),
        ('js', 'JS'),
        ('c++', 'C++'),
    )
    language = forms.ChoiceField(
        choices = CHOICES,
        required = False,
        label = 'Спеціальність'
    )