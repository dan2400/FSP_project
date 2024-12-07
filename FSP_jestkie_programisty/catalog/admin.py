from django.contrib import admin
from .models import SportProgrammingKind, CentralFsp, Region, CompetitionLevel, Competition, RegionalCompetition, NationwideCompetition, SportProgrammingType, Representative, Team, Athlete

@admin.register(CentralFsp)
class CentralFspAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'central_fsp', 'representative_name']

@admin.register(CompetitionLevel)
class CompetitionLevelAdmin(admin.ModelAdmin):
    list_display = ['level_name']

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'description']

@admin.register(RegionalCompetition)
class RegionalCompetitionAdmin(admin.ModelAdmin):
    list_display = ['competition', 'date', 'city', 'region']

@admin.register(NationwideCompetition)
class NationwideCompetitionAdmin(admin.ModelAdmin):
    list_display = ['competition', 'date', 'city', 'region']

@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'region']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_members', 'region', 'competition']

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'registration_date', 'age', 'team']

@admin.register(SportProgrammingKind)
class SportProgrammingKindAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SportProgrammingType)
class SportProgrammingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'regional_competition', 'nationwide_competition')
    search_fields = ('name',)
    list_filter = ('regional_competition', 'nationwide_competition')
    filter_vertical = ('programming_kinds',)