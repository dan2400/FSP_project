from django.db import models

def item_directory_path(instance, filename):
    return f'catalog/{instance.item.id}/{uuid.uuid4()}-{filename}'

# Модель для центрального ФСП
class CentralFsp(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Модель для региона
class Region(models.Model):
    name = models.CharField(max_length=255)
    central_fsp = models.ForeignKey(CentralFsp, related_name='regions', on_delete=models.CASCADE)
    representative_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Модель для общего уровня соревнований
class CompetitionLevel(models.Model):
    level_name = models.CharField(max_length=255)

    def __str__(self):
        return self.level_name


# Модель для соревнований
class Competition(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(CompetitionLevel, related_name='competitions', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    budget = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


# Модель для региональных соревнований
class RegionalCompetition(models.Model):
    competition = models.ForeignKey(Competition, related_name='regional_competitions', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='regional_competitions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competition.name} - {self.city}"


# Модель для всероссийских соревнований
class NationwideCompetition(models.Model):
    competition = models.ForeignKey(Competition, related_name='nationwide_competitions', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='nationwide_competitions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competition.name} - {self.city}"


# Модель для представителей регионов
class Representative(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    region = models.ForeignKey(Region, related_name='representatives', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Модель для команд
class Team(models.Model):
    name = models.CharField(max_length=255)
    number_of_members = models.PositiveIntegerField()
    region = models.ForeignKey(Region, related_name='teams', on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='teams', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Модель для атлетов
class Athlete(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Рекомендуется использовать шифрование паролей
    registration_date = models.DateField(auto_now_add=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, related_name='athletes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Модель для каждого вида спортивного программирования
class SportProgrammingKind(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# Модель для видов спортивного программирования
class SportProgrammingType(models.Model):
    name = models.CharField(max_length=255)
    regional_competition = models.ForeignKey(RegionalCompetition, related_name='sport_programming_types', on_delete=models.CASCADE, null=True, blank=True)
    nationwide_competition = models.ForeignKey(NationwideCompetition, related_name='sport_programming_types', on_delete=models.CASCADE, null=True, blank=True)
    programming_kinds = models.ManyToManyField(SportProgrammingKind, related_name='sport_programming_types', through='SportProgrammingType_programming_kinds')

    def __str__(self):
        return self.name

class SportProgrammingType_programming_kinds(models.Model):
    sport_programming_type = models.ForeignKey('SportProgrammingType', on_delete=models.CASCADE)
    sport_programming_kind = models.ForeignKey('SportProgrammingKind', on_delete=models.CASCADE)