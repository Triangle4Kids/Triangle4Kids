# Generated by Django 2.1.5 on 2019-01-16 17:44

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_merge_20190116_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='age_choice',
            field=models.CharField(choices=[('all_ages', 'All Ages'), ('preschool', 'Pre-K'), ('k_5', 'Elementary'), ('middle_school', 'Middle School'), ('high_school', 'High School')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='type_choice',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('day_camps', 'Day Camps'), ('residential_camps', 'Residential Camps'), ('track_out_program', 'Track-Out Programs'), ('half_day', 'Half-Day'), ('full_day', 'Full-Day'), ('academics', 'Academics'), ('animal_care', 'Animal Care'), ('arts_crafts', 'Arts & Crafts'), ('cooking_baking', 'Cooking & Baking'), ('games', 'Games'), ('health_fitness', 'Health & Fitness'), ('outdoor_play_nature', 'Outdoor & Nature'), ('performing_arts', 'Performing Arts'), ('sports', 'Sports'), ('technology', 'Technology'), ('other', 'Other')], max_length=193, null=True),
        ),
    ]