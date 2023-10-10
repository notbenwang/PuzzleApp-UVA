from django.db import models

class CustomUser(models.Model):
    social_id = models.IntegerField("oauth_id", default=-1)
    is_admin = models.BooleanField("is_admin")

class Puzzle(models.Model):
    prompt_text = models.CharField(max_length=200)