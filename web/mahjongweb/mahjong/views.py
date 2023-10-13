from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *

class battle_withname:
    def __init__(self,u1,u2,u3,u4,p1,p2,p3,p4,date):
        self.User1 = u1
        self.User2 = u2
        self.User3 = u3
        self.User4 = u4
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3
        self.point4 = p4
        self.date = date


class opponent_statistics:
    def __init__(self,name):
        self.Username = name
        self.rivalvalue = 0
        self.encountertime = 0
        self.winrate = 0
        self.oppo1time = 0
        self.oppo2time = 0
        self.oppo3time = 0
        self.oppo4time = 0
        self.oppo1rate = 0
        self.oppo2rate = 0
        self.oppo3rate = 0
        self.oppo4rate = 0
        self.oppoavg = 0
        self.self1time = 0
        self.self2time = 0
        self.self3time = 0
        self.self4time = 0
        self.self1rate = 0
        self.self2rate = 0
        self.self3rate = 0
        self.self4rate = 0
        self.selfavg = 0


def opponents_add_statistics(opponents,opponame,opporank,selfrank):
    found = False
    for o in opponents:
        if o.Username == opponame:
            found = True
            o.encountertime += 1
            if opporank > selfrank:
                o.winrate += 1
            if opporank == 1:
                o.oppo1time += 1
            elif opporank == 2:
                o.oppo2time += 1
            elif opporank == 3:
                o.oppo3time += 1
            elif opporank == 4:
                o.oppo4time += 1
            if selfrank == 1:
                o.self1time += 1
            elif selfrank == 2:
                o.self2time += 1
            elif selfrank == 3:
                o.self3time += 1
            elif selfrank == 4:
                o.self4time += 1
    if not found:
        o = opponent_statistics(opponame)
        o.encountertime += 1
        if opporank > selfrank:
            o.winrate += 1
        if opporank == 1:
            o.oppo1time += 1
        elif opporank == 2:
            o.oppo2time += 1
        elif opporank == 3:
            o.oppo3time += 1
        elif opporank == 4:
            o.oppo4time += 1
        if selfrank == 1:
            o.self1time += 1
        elif selfrank == 2:
            o.self2time += 1
        elif selfrank == 3:
            o.self3time += 1
        elif selfrank == 4:
            o.self4time += 1
        opponents.append(o)

def sort_func(o):
    return o.rivalvalue

def battles_show_name(filter_qq):
    ret = []
    for b in Battle.objects.all().order_by("-date"):
        u1 = User.objects.get(qqnumber=b.User1)
        u2 = User.objects.get(qqnumber=b.User2)
        u3 = User.objects.get(qqnumber=b.User3)
        u4 = User.objects.get(qqnumber=b.User4)
        if filter_qq != None:
            if b.User1 != filter_qq and b.User2 != filter_qq and b.User3 != filter_qq and b.User4 != filter_qq:
                continue
        ret.append(
            battle_withname(u1.Username,u2.Username,u3.Username,u4.Username,
                            b.point1,b.point2,b.point3,b.point4,b.date)
        )
    return ret
updanRule = \
[
    [7, 2.9, 20],
    [7, 2.8, 19],
    [10, 2.7, 27],
    [10, 2.7, 27],
    [12, 2.6, 31],
	[16, 2.6, 41],
	[16, 2.5, 40],
	[20, 2.5, 50],
	[25, 2.4, 60],
	[25, 2.4, 60],
	[30, 2.3, 69],
	[40, 2.1, 84],
	[45, 2.0, 90],
	[50, 1.9, 95]
]

def index(request):
    usernum = len(User.objects.all())
    battlenum = len(Battle.objects.all())
    template = loader.get_template("mahjong/index.html")
    context = {
        "usernum": usernum,
        "battlenum": battlenum,
    }
    return HttpResponse(template.render(context, request))

def statistics(request):
    battles = battles_show_name(None)
    template = loader.get_template("mahjong/statistics.html")
    context = {
        "battles": battles,
    }
    return HttpResponse(template.render(context, request))

def user_id(request, qqnumber):
    the_user = User.objects.get(qqnumber=qqnumber)
    return user(request,the_user.Username)

def user(request, name):
    try:
        user = User.objects.get(Username=name)
        template = loader.get_template("mahjong/user.html")
        yakumans = yakuman.objects.filter(qqnumber=user.qqnumber)
        if user.alltime == 0:
            context = {
                "user": user,
                "firstrate": "-",
                "secondrate": "-",
                "thirdrate": "-",
                "forthrate": "-",
                "battles": [],
                "averageorder": "-",
                "shunweihe": 0,
                "junshun": "-",
                "Updantime": updanRule[user.dan][0],
                "Updanjunshun": updanRule[user.dan][1],
                "Updanshunweihe": updanRule[user.dan][2],
                "averagepoint": "-",
                "beifeicishu": 0,
                "beifeilv": "-",
                "yakumans": yakumans
            }
            return HttpResponse(template.render(context, request))
        battles = battles_show_name(user.qqnumber)
        yakumans = yakuman.objects.filter(qqnumber=user.qqnumber)
        template = loader.get_template("mahjong/user.html")
        points = 0
        beifeicishu = 0
        for b in battles:
            if user.Username == b.User1:
                pt = b.point1
            if user.Username == b.User2:
                pt = b.point2
            if user.Username == b.User3:
                pt = b.point3
            if user.Username == b.User4:
                pt = b.point4
            points += pt
            if pt < 0:
                beifeicishu += 1
        if user.timebeforeupdan == 0:
            shunweihe = 0
        else:
            battles_dan = battles_show_name(user.qqnumber)[:user.timebeforeupdan]
            shunweihe = 0
            for b in battles_dan:
                if user.Username == b.User1:
                    shunwei = 1
                if user.Username == b.User2:
                    shunwei = 2
                if user.Username == b.User3:
                    shunwei = 3
                if user.Username == b.User4:
                    shunwei = 4
                shunweihe += shunwei
        if user.timebeforeupdan!= 0:
            junshun = shunweihe/user.timebeforeupdan
        else:
            junshun = "-"
        context = {
            "user": user,
            "firstrate": round(user.firstplacetime/user.alltime*100,2),
            "secondrate": round(user.secondplacetime/user.alltime*100,2),
            "thirdrate": round(user.thirdplacetime/user.alltime*100,2),
            "forthrate": round(user.forthplacetime/user.alltime*100,2),
            "battles": battles,
            "averageorder": round((user.firstplacetime+2*user.secondplacetime+3*user.thirdplacetime+4*user.forthplacetime)/user.alltime,2),
            "shunweihe": shunweihe,
            "junshun": junshun,
            "Updantime": updanRule[user.dan][0],
            "Updanjunshun": updanRule[user.dan][1],
            "Updanshunweihe": updanRule[user.dan][2],
            "averagepoint": points/user.alltime,
            "beifeicishu": beifeicishu,
            "beifeilv": beifeicishu/user.alltime*100,
            "yakumans": yakumans
        }
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template("mahjong/nouser.html")
        context = {
            "name": name,
        }
        return HttpResponse(template.render(context, request))
    # user = User.objects.get(Username=name)
    # battles = battles_show_name(user.qqnumber)
    # template = loader.get_template("mahjong/user.html")
    # context = {
    #     "user": user,
    #     "firstrate": round(user.firstplacetime/user.alltime*100,2),
    #     "secondrate": round(user.secondplacetime/user.alltime*100,2),
    #     "thirdrate": round(user.thirdplacetime/user.alltime*100,2),
    #     "forthrate": round(user.forthplacetime/user.alltime*100,2),
    #     "battles": battles,
    #     "averageorder" : round((user.firstplacetime+2*user.secondplacetime+3*user.thirdplacetime+4*user.forthplacetime)/user.alltime,2)
    # }
    # return HttpResponse(template.render(context, request))


def users(request):
    users = User.objects.all().order_by("-dan", "-rate")
    template = loader.get_template("mahjong/users.html")
    context = {
        "users": users
    }
    return HttpResponse(template.render(context, request))

def help(request):
    template = loader.get_template("mahjong/help.html")
    context = {}
    return HttpResponse(template.render(context, request))

def rival(request, name):
    try:
        opponents = []
        user = User.objects.get(Username=name)
        battles = battles_show_name(user.qqnumber)
        for b in battles:
            if b.User1 == name:
                opponents_add_statistics(opponents,b.User2,2,1)
                opponents_add_statistics(opponents,b.User3,3,1)
                opponents_add_statistics(opponents,b.User4,4,1)
            if b.User2 == name:
                opponents_add_statistics(opponents,b.User1,1,2)
                opponents_add_statistics(opponents,b.User3,3,2)
                opponents_add_statistics(opponents,b.User4,4,2)
            if b.User3 == name:
                opponents_add_statistics(opponents,b.User1,1,3)
                opponents_add_statistics(opponents,b.User2,2,3)
                opponents_add_statistics(opponents,b.User4,4,3)
            if b.User4 == name:
                opponents_add_statistics(opponents,b.User1,1,4)
                opponents_add_statistics(opponents,b.User2,2,4)
                opponents_add_statistics(opponents,b.User3,3,4)
        for o in opponents:
            oppoallrank = o.oppo1time+2*o.oppo2time+3*o.oppo3time+4*o.oppo4time
            selfallrank = o.self1time+2*o.self2time+3*o.self3time+4*o.self4time
            o.rivalvalue = selfallrank - oppoallrank
            o.oppoavg = oppoallrank/o.encountertime
            o.selfavg = selfallrank/o.encountertime
            o.oppo1rate = o.oppo1time/o.encountertime*100
            o.oppo2rate = o.oppo2time/o.encountertime*100
            o.oppo3rate = o.oppo3time/o.encountertime*100
            o.oppo4rate = o.oppo4time/o.encountertime*100
            o.self1rate = o.self1time/o.encountertime*100
            o.self2rate = o.self2time/o.encountertime*100
            o.self3rate = o.self3time/o.encountertime*100
            o.self4rate = o.self4time/o.encountertime*100
            o.winrate = o.winrate/o.encountertime*100
        opponents.sort(key=sort_func,reverse=True)
        template = loader.get_template("mahjong/rival.html")
        context = {
            "opponents": opponents,
            "name": name,
        }
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template("mahjong/nouser.html")
        context = {
            "name": name,
        }
        return HttpResponse(template.render(context, request))


def majsoul_contest(request):
    template = loader.get_template("mahjong/majsoulusers.html")
    users = Majsouluser.objects.all().order_by("-pt")
    battles = Majsoulbattle.objects.all()
    doranum = 0
    for b in battles:
        doranum += b.doranum
    context = {
        "users": users,
        "doranum": doranum
    }
    return HttpResponse(template.render(context, request))
