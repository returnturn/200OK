# Generated by Django 2.2.2 on 2020-04-03 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200403_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default='9da0b348-5820-41e8-9715-01a8823e9db1', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
