# Generated by Django 2.1.5 on 2019-01-14 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190114_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='zipcode',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
