from django.db import models

class Vacancy(models.Model):
    job_id = models.BigIntegerField()
    company = models.CharField(max_length=128)
    salary = models.BigIntegerField()
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    
    def __str__(self):
        return f'Graph #{self.job_id}'

class Graph(models.Model):
    keyword = models.CharField(max_length=64)
    data = models.JSONField()

    def __str__(self):
        return self.keyword.capitalize()
    
class Skill(models.Model):
    skill = models.CharField(max_length=64)

    def __str__(self):
        return self.skill.capitalize()
    
class Vacancy_skill(models.Model):
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

class Skill_phrase(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    phrase = models.CharField(max_length=128)