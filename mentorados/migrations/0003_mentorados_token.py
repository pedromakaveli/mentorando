# Generated by Django 5.1.7 on 2025-04-06 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorados', '0002_disponibilidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorados',
            name='token',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
