# Generated by Django 2.2.4 on 2019-11-14 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projeto', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproject',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.User'),
        ),
        migrations.AddField(
            model_name='projectimage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projeto.Project'),
        ),
        migrations.AddField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(to='projeto.Category'),
        ),
    ]
