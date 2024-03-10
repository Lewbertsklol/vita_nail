from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True, primary_key=True)

    def __str__(self) -> str:
        return f'{self.name} {self.surname} {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Window(models.Model):
    date = models.DateTimeField(unique=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'
        verbose_name = 'Окошко'
        verbose_name_plural = 'Окошки'

    def __str__(self) -> str:
        return f'{self.date} - {self.client if self.client else "свободно"}'


class Work(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    window = models.ForeignKey(Window, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.IntegerField()
    comment = models.TextField(default=None, blank=True, null=True)
    date_to_remind = models.DateField(blank=True, null=True)
