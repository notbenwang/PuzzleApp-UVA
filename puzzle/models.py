from django.db import models

class CustomUser(models.Model):
    social_id = models.IntegerField("oauth_id", default=-1)
    is_admin = models.BooleanField("is_admin")
