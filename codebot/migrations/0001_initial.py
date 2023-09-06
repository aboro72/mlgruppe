# Generated by Django 4.2 on 2023-04-25 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Code",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField(max_length=5000)),
                ("code_answer", models.TextField(max_length=5000)),
                ("language", models.CharField(max_length=50)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="code",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
