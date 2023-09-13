# Generated by Django 4.2.4 on 2023-09-13 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '0001_initial'),
        ('pit', '0012_remove_ansprechpartner_kunde_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schiene',
            name='status',
            field=models.CharField(choices=[('Lager', 'Lager'), ('Unterwegs', 'Unterwegs'), ('Zurücksetzen', 'Zurücksetzen'), ('Imagen', 'Imagen'), ('Versand', 'Versand'), ('Standort', 'Standort'), ('Rückholung', 'Rückholung'), ('Weiterleitung', 'Weiterleitung'), ('Selbstabholung', 'Selbstabholung')], max_length=255),
        ),
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.CharField(choices=[('Lager', 'Lager'), ('Unterwegs', 'Unterwegs'), ('Zurücksetzen', 'Zurücksetzen'), ('Versand', 'Versand'), ('Standort', 'Standort'), ('Rückholung', 'Rückholung'), ('Weiterleitung', 'Weiterleitung'), ('Selbstabholung', 'Selbstabholung')], default='Zurücksetzen', max_length=255),
        ),
        migrations.CreateModel(
            name='Abholung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Vorname', models.CharField(blank=True, max_length=255, null=True)),
                ('Mobile', models.CharField(max_length=17)),
                ('Email', models.CharField(blank=True, max_length=255, null=True)),
                ('Firmenwagen', models.BooleanField(default=True)),
                ('Datum', models.DateField(blank=True, null=True)),
                ('Kunde', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kunden.kunde')),
                ('Schiene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pit.schiene')),
                ('Server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pit.server')),
            ],
        ),
    ]