from django.contrib.auth import get_user_model
from django.db import models

from breaks.constants import BREAK_DEFAULT_STATUS, BREAK_DEFAULT_STATUS_EXTRA
from breaks.models.dicts import BreakStatus

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey('breaks.Replacement', models.CASCADE, 'breaks', verbose_name='Смена')
    employee = models.ForeignKey(User, models.CASCADE, 'breaks', verbose_name='Сотрудник')
    break_start = models.TimeField('Начало обеда')
    break_end = models.TimeField('Конец обеда')
    status = models.ForeignKey('breaks.BreakStatus', models.RESTRICT, 'breaks', verbose_name='Статус', null=False, blank=True)

    class Meta:
        verbose_name = 'Обеденный перерыв'
        verbose_name_plural = 'Обеденные перерывы'
        ordering = '-replacement__date', 'break_start'

    def __str__(self):
        return f'Обед пользователя {self.employee} ({self.pk})'

    def save(self, *args, **kwargs):
        # pdb.set_trace()
        if not self.pk:
            status, created = BreakStatus.objects.get_or_create(
                code=BREAK_DEFAULT_STATUS,
                defaults=BREAK_DEFAULT_STATUS_EXTRA
            )
            self.status = status
        return super(Break, self).save(*args, **kwargs)
