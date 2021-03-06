# Generated by Django 2.2.2 on 2020-04-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0012_auto_20200403_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('text/markdown', 'Markdown'), ('text/plain', 'Plain Text')], default='text/plain', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('text/plain', 'Plain text'), ('image/png;base64', 'Image/png'), ('image/jpeg;base64', 'Image/jpeg'), ('text/markdown', 'Markdown'), ('application/base64', 'Application')], default='text/plain', max_length=20),
        ),
    ]
