# Generated by Django 2.2.2 on 2020-04-03 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200402_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default='fbb2d42d-5df5-489c-8f93-5bd343e4504b', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]