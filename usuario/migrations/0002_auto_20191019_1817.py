# Generated by Django 2.2.4 on 2019-10-19 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contato', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contacts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contato.Contact', unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='endereco.Address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(blank=True, max_length=250, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='UsuarioContato',
        ),
    ]