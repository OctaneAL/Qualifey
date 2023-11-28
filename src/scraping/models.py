from django.db import models

class Vacancy(models.Model):
    job_id = models.CharField(max_length=128)
    # company = models.CharField(max_length=128, blank = True, null = True)
    # company = models.ForeignKey('Company', on_delete=models.CASCADE, null = True)
    # salary = models.BigIntegerField(blank = True, null = True)
    # country = models.CharField(max_length=64, blank = True, null = True)
    # city = models.CharField(max_length=64, blank = True, null = True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null = True, default = None)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null = True, default = None)

    source = models.ForeignKey('Source', on_delete=models.CASCADE, null = True, default = None)
    timestamp = models.DateTimeField(null = True, default = None)
    # timestamp = models.DateTimeField(null = True, default = None)

    # has_salary = models.BooleanField(blank = True, null = True, default = None)
    # salary_min = models.IntegerField(blank = True, null = True, default = None)
    # salary_max = models.IntegerField(blank = True, null = True, default = None)
    # yearly_salary = models.BooleanField(blank = True, null = True, default = None)
    
    def __str__(self):
        return str(self.job_id)
    
class JobTitle(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)
    
class OccupationUri(models.Model):
    link = models.CharField(max_length=128)
    jobtitle = models.ForeignKey('JobTitle', on_delete=models.CASCADE)

    # def __str__(self):
    #     return str(JobTitle.objects.get(id = self.jobtitle_id).name)

class State(models.Model):
    abbreviation = models.CharField(max_length=2, blank=True, unique=True)
    name = models.CharField(max_length=64, blank=True)
    # country ????

    def __str__(self):
        return str(self.name)

class AvailableVacancies(models.Model):
    count = models.BigIntegerField()
    jobtitle = models.ForeignKey('JobTitle', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.timestamp)
    
class Source(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)

# class City(models.Model):
#     name = models.CharField(max_length=64, blank=True, unique=True)
#     male_population = models.BigIntegerField(blank=True, default=0)
#     female_population = models.BigIntegerField(blank=True, default=0)
#     population = models.BigIntegerField(blank=True, default=0)
#     state = models.ForeignKey('State', on_delete=models.CASCADE, null=True)
#     country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return str(self.name)

class Continent(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)
    
class Country(models.Model):
    abbreviation = models.CharField(max_length=5, blank=True, unique=True)
    name = models.CharField(max_length=64, blank=True)
    
    # continent = models.ForeignKey('Continent', on_delete=models.CASCADE, null = True, default = None)
    # population = models.BigIntegerField(blank=True, default=0)
    # gdp_usd = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.name)

class Company(models.Model):
    name = models.CharField(max_length=64, blank=True)
    # country ????

    def __str__(self):
        return str(self.name)

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
    
# class Vacancy_skill(models.Model):
#     vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE)
#     skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.vacancy} - {self.skill}'

class Skill_phrase(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    phrase = models.CharField(max_length=128)

    def __str__(self):
        return self.phrase