from django.contrib import admin
from .models import OccupationUri, JobTitle, Vacancy, Graph, Skill, Skill_phrase, Country, State, Company

# Register your models here.
admin.site.register(Vacancy)
# admin.site.register(Vacancy_skill)
admin.site.register(Graph)
admin.site.register(Skill)
admin.site.register(Skill_phrase)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Company)
# admin.site.register(City)
admin.site.register(JobTitle)
admin.site.register(OccupationUri)