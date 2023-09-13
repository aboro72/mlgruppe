from django.db import models


# Create your models here.


class Trainer(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Vorname = models.CharField(max_length=100, null=True, blank=True)
    Outlook = models.BooleanField(default=False)
    SharePoint = models.BooleanField(default=False)
    SMS = models.BooleanField(default=False)
    Mobil = models.CharField(max_length=17, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.Name + ", " + self.Vorname

        class Meta:
            verbose_name = "Trainer"
            verbose_name_plural = "Trainers"
            ordering = ["Name"]


