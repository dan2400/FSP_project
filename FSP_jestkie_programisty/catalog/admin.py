from django.contrib import admin
from catalog.models import SportProgrammingKind, CentralFsp, Region, CompetitionLevel, Competition, RegionalCompetition, NationwideCompetition, SportProgrammingType, Representative, Team, Athlete

@admin.register(CentralFsp)
class CentralFspAdmin(admin.ModelAdmin):
    list_display = ()
    list_admin = ('name', 'description')
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.list_display + self.list_admin
        else:
            self.fields = self.list_display
        return super(CentralFspAdmin, self).get_form(request, obj, **kwargs)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ()
    list_admin = ('name', 'central_fsp', 'representative_name')
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.list_display + self.list_admin
        else:
            self.fields = self.list_display
        return super(RegionAdmin, self).get_form(request, obj, **kwargs)

@admin.register(CompetitionLevel)
class CompetitionLevelAdmin(admin.ModelAdmin):
    list_display = ['level_name']


class RegionalCompetitionAdmin(admin.TabularInline):
    model = RegionalCompetition


class NationwideCompetitionAdmin(admin.TabularInline):
    model = NationwideCompetition

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    model = Competition
    list_display = ('name', 'level', 'description', 'is_active', 'budget')
    list_admin = ('is_active', 'budget')
    def get_form(self, request, obj=None, **kwargs):

        if request.user.groups.filter(name='worker').exists():
            self.fields = self.list_display + self.list_admin
        elif request.user.groups.filter(name='center_admin').exists():
            self.fields = self.list_display + self.list_admin
            self.inlines = (NationwideCompetitionAdmin, RegionalCompetitionAdmin)
        elif request.user.groups.filter(name='region_admin').exists():
            self.fields = self.list_display + self.list_admin
            self.inlines = (RegionalCompetitionAdmin,)
        else:
            self.fields = self.list_display
            self.readonly_fields = self.list_admin
        return super(CompetitionAdmin, self).get_form(request, obj, **kwargs)


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
