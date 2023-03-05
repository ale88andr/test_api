from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Organisation(models.Model):
    name = models.CharField('Наименование', max_length=255)
    director = models.ForeignKey(User, models.RESTRICT, 'organisations_directors', verbose_name='Директор')
    employees = models.ManyToManyField(User, 'organisations_employees', verbose_name='Сотрудники', blank=True, through='Employee')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = 'name',

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Group(models.Model):
    organisation = models.ForeignKey('Organisation', models.CASCADE, 'groups', verbose_name='Организация')
    name = models.CharField('Наименование', max_length=255)
    manager = models.ForeignKey(User, models.RESTRICT, 'groups_managers', verbose_name='Менеджер')
    members = models.ManyToManyField(User, 'groups_members', verbose_name='Участники групп', blank=True, through='Member')


    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = 'name',

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Employee(models.Model):
    organisation = models.ForeignKey('Organisation', models.CASCADE, 'employees_info')
    user = models.ForeignKey(User, models.CASCADE, 'organisations_info')
    position = models.ForeignKey('Position', models.RESTRICT, 'employees')
    date_joined = models.DateField('Присоединен', default=timezone.now)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = '-date_joined',
        unique_together = (('organisation', 'user'),)

    def __str__(self):
        return f'Employee {self.user}'


class Member(models.Model):
    group = models.ForeignKey('Group', models.CASCADE, 'members_info')
    user = models.ForeignKey(User, models.CASCADE, 'groups_info')
    date_joined = models.DateField('Присоединен', default=timezone.now)

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        ordering = '-date_joined',
        unique_together = (('group', 'user'),)

    def __str__(self):
        return f'Employee {self.user}'

