# Generated by Django 4.2.13 on 2024-05-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleapp', '0007_globalnumbers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
