# Generated by Django 4.2.13 on 2024-05-16 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleapp', '0005_globalnumbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalnumbers',
            name='is_spam',
            field=models.BooleanField(default=False),
        ),
    ]