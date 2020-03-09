# Generated by Django 2.1.5 on 2020-03-09 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20200309_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default='9adfc919-2637-4d8d-b37d-0b812d0c1a45', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(default='9adfc919-2637-4d8d-b37d-0b812d0c1a45', max_length=100),
        ),
    ]
