from django.db import models

class CustomUser(models.Model):
    social_id = models.IntegerField("oauth_id", default=-1)
    is_admin = models.BooleanField("is_admin")

class Hunt(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=2000)
    approved = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)

class Puzzle(models.Model):
    prompt_text = models.CharField(max_length=200)
    hunt_id= models.ForeignKey(Hunt, on_delete=models.CASCADE, default = 0)
    long = models.FloatField(default = 0) 
    lat = models.FloatField(default = 0)
    radius = models.IntegerField(default = 10)
    order = models.IntegerField(default = -1)

class Hint(models.Model):
    hint_string = models.CharField(max_length=500)
    puzzle_id = models.ForeignKey(Puzzle, on_delete=models.CASCADE, default = 0)