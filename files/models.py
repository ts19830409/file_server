from django.db import models

class File(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='files',
                             verbose_name='Пользователь')
    

