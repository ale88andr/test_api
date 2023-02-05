from django.contrib import admin
from django.contrib.admin import TabularInline

from breaks.models import organisations, replacements


####################
# Inlines
####################
class ReplacementEmployeeInline(TabularInline):
    model = replacements.ReplacementEmployee
    fields = 'employee', 'status',


####################
# Models
####################
@admin.register(organisations.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'director',


@admin.register(organisations.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'manager', 'min_active',


@admin.register(replacements.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = 'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration',
    inlines = ReplacementEmployeeInline,


@admin.register(replacements.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'sort', 'is_active',
