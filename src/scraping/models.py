from django.db import models

class Vacancy(models.Model):
    job_id = models.CharField(max_length=128)
    # company = models.CharField(max_length=128, blank = True, null = True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null = True)
    # salary = models.BigIntegerField(blank = True, null = True)
    country = models.CharField(max_length=64, blank = True, null = True)
    city = models.CharField(max_length=64, blank = True, null = True)

    has_salary = models.BooleanField(blank = True, null = True, default = None)
    salary_min = models.IntegerField(blank = True, null = True, default = None)
    salary_max = models.IntegerField(blank = True, null = True, default = None)
    yearly_salary = models.BooleanField(blank = True, null = True, default = None)
    
    def __str__(self):
        return str(self.job_id)
    
class Company(models.Model):
    name = models.CharField(max_length=128, blank=True)

class Graph(models.Model):
    skill = models.OneToOneField(
        'Skill',
        on_delete=models.CASCADE,
        default=None
    )
    data = models.JSONField()

    def __str__(self):
        return Skill.objects.get(id = self.skill_id).skill
    
class Skill(models.Model):
    skill = models.CharField(
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.skill
    
class Vacancy_skill(models.Model):
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vacancy} - {self.skill}'

class Skill_phrase(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    phrase = models.CharField(max_length=128)

    def __str__(self):
        return self.phrase