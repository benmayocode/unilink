# Generated by Django 3.0.8 on 2020-08-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='id',
        ),
        migrations.AddField(
            model_name='todo',
            name='task_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
