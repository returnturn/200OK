# Generated by Django 2.2.2 on 2020-04-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200403_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default='fde27499-cc28-46ac-9d35-7bf61c3154a1', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
