import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from polls.models import *
from datetime import date
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False

def recordbattle(ptdict):
    sorteddict = sorted(ptdict.items(),  key=lambda d: d[1], reverse=True)
    battle = Battle.objects.create(
        User1=sorteddict[0][0],
        User2=sorteddict[1][0],
        User3=sorteddict[2][0],
        User4=sorteddict[3][0],
        points1=sorteddict[0][1],
        points2=sorteddict[1][1],
        points3=sorteddict[2][1],
        points4=sorteddict[3][1],
        data=timezone.now(),
    )

def checkadduser(Users):
    updated = []
    for u in Users:
        try:
            user = User.objects.get(qqnumber=str(u[0]))
        except:
            user = User.objects.create(qqnumber=str(u[0]),Username=u[1])
            updated.append(u[1])
    return updated
