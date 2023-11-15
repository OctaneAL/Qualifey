from django.contrib import admin
from .models import Vacancy, Vacancy_skill, Graph, Skill, Skill_phrase, Country, State, Company, City

# Register your models here.
admin.site.register(Vacancy)
admin.site.register(Vacancy_skill)
admin.site.register(Graph)
admin.site.register(Skill)
admin.site.register(Skill_phrase)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Company)
admin.site.register(City)