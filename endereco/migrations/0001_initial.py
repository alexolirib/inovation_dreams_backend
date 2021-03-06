# Generated by Django 2.2.4 on 2019-10-19 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipCode', models.CharField(blank=True, max_length=8, null=True)),
                ('street', models.CharField(blank=True, max_length=180, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=180, null=True)),
                ('neighbourhood', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=180, null=True)),
                ('complement', models.CharField(blank=True, max_length=180, null=True)),
            ],
        ),
    ]
