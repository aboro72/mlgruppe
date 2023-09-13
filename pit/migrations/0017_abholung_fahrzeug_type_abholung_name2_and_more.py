# Generated by Django 4.2.4 on 2023-09-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pit', '0016_alter_abholung_tourdaten'),
    ]

    operations = [
        migrations.AddField(
            model_name='abholung',
            name='Fahrzeug_Type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='abholung',
            name='Name2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='abholung',
            name='VA_Nummer',
            field=models.IntegerField(default='00000', max_length=8, unique=True),
        ),
        migrations.AddField(
            model_name='abholung',
            name='Vorname2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='abholung',
            name='Firmenwagen',
            field=models.CharField(choices=[('Ja', 'Ja'), ('Privat Fahrzeug', 'Privat Fahrzeug'), ('Mietfahrzeug', 'Mietfahrzeug')], max_length=255),
        ),
    ]