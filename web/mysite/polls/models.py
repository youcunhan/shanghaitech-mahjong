import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class User(models.Model):
    Username = models.CharField(max_length=200)
    qqnumber = models.CharField(max_length=200)


class Battle(models.Model):
    User1 = models.CharField(max_length=200)
    User2 = models.CharField(max_length=200)
    User3 = models.CharField(max_length=200)
    User4 = models.CharField(max_length=200)
    
    points1 = models.IntegerField()
    points2 = models.IntegerField()
    points3 = models.IntegerField()
    points4 = models.IntegerField()
    
    data = models.DateTimeField("date battled")