# Generated by Django 2.2.4 on 2019-09-10 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20190910_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariocontato',
            name='contato',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contato.Contato'),
        ),
    ]