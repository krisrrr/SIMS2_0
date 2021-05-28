from django.conf import settings
from django.db import models
from django.urls import reverse


class UserDeviceData(models.Model):
    user = models.CharField(max_length=150, verbose_name='Пользователь')
    mac_address = models.CharField(max_length=150, verbose_name='MAC-адрес', blank=True)
    auth_key = models.CharField(max_length=150, verbose_name='Ключ аутентификации', blank=True)

    class Meta:
        verbose_name = 'Данные устройства'
        ordering = ['id']


class Activity(models.Model):
    date_time = models.DateTimeField(verbose_name='Дата и время')
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', null=True)
    intensity = models.IntegerField(verbose_name='Аксель', default=0)
    steps = models.IntegerField(verbose_name='Шаги', default=0)
    heart_rate = models.IntegerField(verbose_name='Пульс', default=0)
    category_num = models.IntegerField(verbose_name='Значение категории')
    user = models.CharField(verbose_name='Пользователь', max_length=150)
    is_sleeping = models.IntegerField(blank=True)      # 0 - бодрствование, 1 - сон
    sleep_phase = models.IntegerField(blank=True)      # 0 - бодрствование, 1 - быстрый сон, 2 - глубокий сон

    def __str__(self):
        return self.date_time.strftime('%d.%m.%Y %H:%M:%S')

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Данные активности'
        ordering = ['-date_time']


class Articles(models.Model):
    title = models.CharField(max_length=200)
    article = models.TextField()
    image = models.ImageField(upload_to='photos/')

    def get_absolute_url(self):
        return reverse('articles', kwargs={'article_id': self.pk})

    def __str__(self):
        return self.title


class UserGraphics(models.Model):
    user = models.CharField(max_length=150, verbose_name='username')
    graphic = models.ImageField(upload_to='graphics/')
