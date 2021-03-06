from django.db import models
import datetime


class Team(models.Model):
    TEAM_CHOICES = (
        ('UG', 'UG'),
        ('PG', "PG"),
    )
    YEAR_CHOICES = [(x, x) for x in range(int(datetime.datetime.now().year), 2007, -1)]

    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    team_type = models.CharField(max_length=4, choices=TEAM_CHOICES)
    members = models.ManyToManyField("oauth.UserProfile")

    def __str__(self):
        return self.team_type + self.year
