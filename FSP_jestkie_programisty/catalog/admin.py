from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.sport.field.name,
        catalog.models.Item.country.field.name,
        catalog.models.Item.subject.field.name,
        catalog.models.Item.town.field.name,
        catalog.models.Item.location.field.name,
        catalog.models.Item.time.field.name,
        catalog.models.Item.alert.field.name,
    )
    list_display_links = (catalog.models.Item.name.field.name,)


@admin.register(catalog.models.Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Sport.name.field.name,)


@admin.register(catalog.models.Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Discipline.name.field.name,)


@admin.register(catalog.models.Genage)
class GenageAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Genage.name.field.name,)


@admin.register(catalog.models.Mass)
class MassAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Mass.name.field.name,)


@admin.register(catalog.models.Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Gender.name.field.name,)


@admin.register(catalog.models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Country.name.field.name,)


@admin.register(catalog.models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Subject.name.field.name,)


@admin.register(catalog.models.Town)
class TownAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Town.name.field.name,)


@admin.register(catalog.models.Range_m)
class Range_mAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Range_m.name.field.name,)


__all__ = [
    'MainImage',
    'Image',
    'ItemAdmin',
    'CategoryAdmin',
    'TagAdmin',
]
