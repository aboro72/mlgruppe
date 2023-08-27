from django.db import models
from django.contrib.auth.models import User


class Text(models.Model):
    user = models.ForeignKey(User, related_name="text", on_delete=models.DO_NOTHING)
    question = models.TextField(max_length=5000)
    text_answer = models.TextField(max_length=5000)
    language = models.CharField(max_length=50)
    language2 = models.CharField(max_length=50)

    def __str__(self):
        return self.question
