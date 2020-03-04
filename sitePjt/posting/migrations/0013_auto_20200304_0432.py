# Generated by Django 2.1.5 on 2020-03-04 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0012_auto_20200304_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('text', 'text/plain'), ('md', 'text/markdown')], default='text', max_length=4),
        ),
    ]
