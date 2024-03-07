from django.db import models

# Create your models here.


# class Admin(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=12)
#     token = 


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True)

    def __str__(self) -> str:
        return f'{self.name} {self.surname} {self.phone}'


class Window(models.Model):
    date = models.DateTimeField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

    def __str__(self) -> str:
        return f'{self.date} - {self.user if self.user else "свободно"}'


class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    window = models.ForeignKey(Window, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.IntegerField()
    comment = models.TextField(default=None, blank=True, null=True)
    date_to_remind = models.DateField(blank=True, null=True)
