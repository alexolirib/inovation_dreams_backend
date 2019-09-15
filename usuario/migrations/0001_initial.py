# Generated by Django 2.2.4 on 2019-09-15 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contato', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('idade', models.IntegerField()),
                ('foto', models.CharField(max_length=40, null=True)),
                ('availiacao', models.IntegerField(null=True)),
                ('dt_nascimento', models.DateField()),
                ('naturalidade', models.CharField(max_length=90)),
                ('nacionalidade', models.CharField(max_length=90)),
                ('genero', models.CharField(choices=[(1, 'Masculino'), (2, 'Feminino')], max_length=10)),
                ('estado_civil', models.CharField(choices=[(1, 'Solteiro'), (2, 'Casado'), (3, 'Divorciado'), (4, 'Viúvo')], max_length=10)),
                ('nome_mae', models.CharField(max_length=180)),
                ('nome_pai', models.CharField(max_length=180, null=True)),
                ('cidade_nascimento', models.CharField(max_length=100)),
                ('estado_nascimento', models.CharField(max_length=100)),
                ('cadastro_finalizado', models.BooleanField(default=False)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioContato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contato', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contato.Contato')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario')),
            ],
        ),
    ]
