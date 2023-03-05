from django.contrib import admin
from django.contrib.admin import TabularInline
from django.urls import reverse
from django.utils.html import format_html

from breaks.models import replacements, dicts, breaks


####################
# Inlines
####################
class ReplacementEmployeeInline(TabularInline):
    model = replacements.ReplacementEmployee
    fields = 'employee', 'status',


####################
# Models
####################
@admin.register(replacements.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = 'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration',
    inlines = ReplacementEmployeeInline,
    # autocomplete_fields = 'group',


@admin.register(dicts.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'sort', 'is_active',


@admin.register(dicts.BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'sort', 'is_active',


@admin.register(breaks.Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = '__str__', 'replacement_link', 'break_start', 'break_end',
    list_filter = 'status__name',
    # readonly_fields = 'break_start', 'break_end'
    empty_value_display = 'Unknown'
    radio_fields = {'status': admin.VERTICAL}

    def replacement_link(self, obj):
        link = reverse('admin:breaks_replacement_change', args=[obj.replacement.id])
        return format_html('<a href="{}">{}</a>', link, obj.replacement)
