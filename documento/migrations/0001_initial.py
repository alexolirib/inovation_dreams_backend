# Generated by Django 2.2.4 on 2019-09-15 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_expedicao', models.DateTimeField()),
                ('uf', models.CharField(max_length=2)),
                ('cpf', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='CNH',
            fields=[
                ('documento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documento.Documento')),
                ('num_cnh', models.IntegerField()),
                ('codigo_seguranca', models.IntegerField()),
            ],
            bases=('documento.documento',),
        ),
        migrations.CreateModel(
            name='RG',
            fields=[
                ('documento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documento.Documento')),
                ('num_rg', models.CharField(max_length=13)),
                ('orgao_emissor', models.CharField(max_length=15)),
            ],
            bases=('documento.documento',),
        ),
        migrations.CreateModel(
            name='RNE',
            fields=[
                ('documento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documento.Documento')),
                ('num_rne', models.CharField(max_length=8)),
            ],
            bases=('documento.documento',),
        ),
    ]
