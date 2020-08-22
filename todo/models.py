from django.db import models

# Create your models here.

class ToDo(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_text = models.CharField(max_length=200)
    completed = models.BooleanField()
    created_date = models.DateField('date created')
    due_date = models.DateField('date due')
    username = models.CharField(max_length=200)

class RowOrder(models.Model):
    username = models.CharField(max_length=200)
    row_order = models.CharField(max_length=999999999)
