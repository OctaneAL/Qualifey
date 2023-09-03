from django.contrib import admin
from .models import Vacancy, Vacancy_skill, Graph, Skill

# Register your models here.
admin.site.register(Vacancy)
admin.site.register(Vacancy_skill)
admin.site.register(Graph)
admin.site.register(Skill)