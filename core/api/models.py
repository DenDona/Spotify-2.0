from django.db import models

# Create your models here.
class Music(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    file = models.FileField(verbose_name='Песня', upload_to='tracks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name