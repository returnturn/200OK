# Generated by Django 2.2.2 on 2020-04-01 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200401_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default='ced2fd31-cd1d-4804-abf1-70bb793a5c83', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
