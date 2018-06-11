from django.db import models

# Create your models here.
class Calendar(models.Model):
    comment = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calendar'

class User(models.Model):
    name = models.TextField()
    password = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
