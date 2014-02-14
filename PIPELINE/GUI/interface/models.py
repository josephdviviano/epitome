from django.db import models
import datetime

class Poll(models.Model):
    experiment = models.CharField(max_length=200)
    start_date = models.DateTimeField('date published')

    def __unicode__(self):
    	return self.experiment

    def was_published_today(self):
    	return self.start_date.date() == datetime.date.today()

class Choice(models.Model):
    subjects = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
		return self.choice