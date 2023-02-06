from django.db import models


class BaseDictModelMixin(models.Model):
    code = models.CharField('Код', max_length=16, primary_key=True)
    name = models.CharField('Наименование', max_length=50)
    sort = models.PositiveSmallIntegerField('Сортировка', null=True, blank=True)
    is_active = models.BooleanField('Активность', default=True)

    class Meta:
        ordering = 'sort',
        abstract = True

    def __str__(self):
        return f'{self.code} ({self.name})'
