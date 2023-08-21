# Generated by Django 4.2.4 on 2023-08-19 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strasse', models.CharField(max_length=255)),
                ('plz', models.CharField(max_length=10)),
                ('stadt', models.CharField(max_length=255)),
                ('land', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FestplattenImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('beschreibung', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kunde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('typ', models.CharField(choices=[('Firma', 'Firma'), ('Behörde', 'Behörde')], max_length=255)),
                ('adresse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pit.adresse')),
            ],
        ),
        migrations.CreateModel(
            name='Schiene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('Lager', 'Lager'), ('Unterwegs', 'Unterwegs'), ('Zurücksetzen', 'Zurücksetzen'), ('Imagen', 'Imagen')], max_length=255)),
                ('DruckerFuellstandA', models.IntegerField(default=100)),
                ('DruckerFuellstandB', models.IntegerField(default=100)),
                ('Nighthawk', models.CharField(default='Beispiel: NH 01', max_length=10)),
                ('datum_kms_aktivierung', models.DateField()),
                ('Bemerkung', models.TextField(default='Fehler/Bemerkung', max_length=500)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pit.festplattenimage')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('Lager', 'Lager'), ('Unterwegs', 'Unterwegs'), ('Zurücksetzen', 'Zurücksetzen'), ('Unbekannt', 'Unbekannt')], default='Zurücksetzen', max_length=255)),
                ('Bemerkung', models.TextField(default='Fehler/Bemerkung', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('adresse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pit.adresse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchieneBewegung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_versand', models.DateField()),
                ('rueckholung_datum', models.DateField(blank=True, null=True)),
                ('weiterleitung_datum', models.DateField(blank=True, null=True)),
                ('kunde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pit.kunde')),
                ('schiene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pit.schiene')),
                ('weiterleitung_adresse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weiterleitung_adresse', to='pit.adresse')),
                ('weiterleitung_kunde', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weiterleitung_kundr', to='pit.kunde')),
                ('ziel_adresse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ziel_adresse', to='pit.adresse')),
            ],
        ),
        migrations.CreateModel(
            name='Kurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kurz_art', models.CharField(max_length=255)),
                ('va_nummer', models.CharField(max_length=255, unique=True)),
                ('kunde', models.ForeignKey(default='Ich bin eine Beispiel Kaserne', on_delete=django.db.models.deletion.CASCADE, to='pit.kunde')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pit.trainer')),
            ],
        ),
    ]
