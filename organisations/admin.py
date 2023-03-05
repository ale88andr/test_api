from django.contrib import admin
from django.db.models import Count

from breaks.models.replacements import GroupInfo
from organisations.models import organisations, dicts


####################
# Inlines
####################
class EmployeeInline(admin.TabularInline):
    model = organisations.Employee
    fields = 'user', 'position', 'date_joined'


class MemberInline(admin.TabularInline):
    model = organisations.Member
    fields = 'user', 'date_joined'


class GroupInfoInLine(admin.StackedInline):
    model = GroupInfo
    fields = 'min_active', 'break_start', 'break_end', 'break_max_duration'


####################
# Models
####################
@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'sort', 'is_active',


@admin.register(organisations.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'director',
    filter_horizontal = 'employees',
    inlines = (EmployeeInline,)


@admin.register(organisations.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'manager', 'replacement_count',
    list_display_links = 'id', 'name',
    search_fields = 'name',
    inlines = (MemberInline, GroupInfoInLine)

    def replacement_count(self, obj):
        return obj.replacement_count

    replacement_count.short_description = 'Кол-во смен'

    def get_queryset(self, request):
        return organisations.Group.objects.annotate(replacement_count=Count('replacements__id'))
