# Generated by Django 4.2.6 on 2024-01-28 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_doctor_unique_slug_category'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='doctor',
            name='unique_slug_category',
        ),
    ]