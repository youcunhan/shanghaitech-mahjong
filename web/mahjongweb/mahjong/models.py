import datetime
import os
import time
from django.db import models
from django.utils import timezone

def modify_path(instance, filename):
    '''
    重定义图片保存路径
    :param instance: self
    :param filename: 文件名
    :return: 新路径
    '''
    ext = filename.split('.').pop()
    now_date = datetime.datetime.now().strftime('%Y%m%d')
    now_time = int(time.time())
    filename = '{0}{1}.{2}'.format(now_date, now_time, ext)
    return os.path.join('yakuman_photo', now_date, filename)

class User(models.Model):
    Username = models.CharField(max_length=200)
    qqnumber = models.CharField(max_length=200)

    rate = models.FloatField()

    firstplacetime = models.IntegerField()
    secondplacetime = models.IntegerField()
    thirdplacetime = models.IntegerField()
    forthplacetime = models.IntegerField()
    alltime = models.IntegerField()

    timebeforeupdan = models.IntegerField()

    dan = models.IntegerField()

class Battle(models.Model):
    User1 = models.CharField(max_length=200)
    User2 = models.CharField(max_length=200)
    User3 = models.CharField(max_length=200)
    User4 = models.CharField(max_length=200)
    
    point1 = models.IntegerField()
    point2 = models.IntegerField()
    point3 = models.IntegerField()
    point4 = models.IntegerField()
    
    date = models.DateTimeField("date battled")

class yakuman(models.Model):
    date = models.DateTimeField("date recorded")
    qqnumber = models.CharField(max_length=200)
    yakuman_type = models.CharField(max_length=200)
    yakuman_photo = models.ImageField(upload_to=modify_path,null=True,blank=True)


class Majsouluser(models.Model):
    nickname = models.CharField(max_length=200)

    pt = models.FloatField()

class Majsoulbattle(models.Model):
    User1 = models.CharField(max_length=200)
    User2 = models.CharField(max_length=200)
    User3 = models.CharField(max_length=200)

    point1 = models.FloatField()
    point2 = models.FloatField()
    point3 = models.FloatField()

    doranum = models.IntegerField()

    uuid = models.CharField(max_length=200)

    date = models.DateTimeField("date battled")
