# Generated by Django 2.1.5 on 2019-01-07 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('average_rating', models.FloatField(default='0')),
                ('link', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Businesses',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('start_time', models.CharField(max_length=255)),
                ('end_time', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.Business')),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='LeaveReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('rating', models.IntegerField(default='0')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.Business')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='core.Event')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
