# Generated by Django 2.2.4 on 2019-11-03 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0006_auto_20191102_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
