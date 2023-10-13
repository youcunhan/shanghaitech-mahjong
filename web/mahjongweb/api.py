import os,django
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mahjongweb.settings")
django.setup()
from mahjong.models import *
from datetime import date
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
class battle_withname:
    def __init__(self,u1,u2,u3,u4,p1,p2,p3,p4):
        self.User1 = u1
        self.User2 = u2
        self.User3 = u3
        self.User4 = u4
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3
        self.point4 = p4

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
                            b.point1,b.point2,b.point3,b.point4)
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
dans = ["新人", "5级", "4级", "3级", "2级", "1级", "初段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段"]
def checkUpDan(u:User):
    if u.timebeforeupdan < updanRule[u.dan][0] or u.dan == 14:
        return
    else:
        battles = battles_show_name(u.qqnumber)[:updanRule[u.dan][0]]
        shunweihe = 0
        for b in battles:
            if u.Username == b.User1:
                shunwei = 1
            if u.Username == b.User2:
                shunwei = 2
            if u.Username == b.User3:
                shunwei = 3
            if u.Username == b.User4:
                shunwei = 4
            shunweihe += shunwei
        junshun = shunweihe/updanRule[u.dan][0]
        if junshun <= updanRule[u.dan][1] and shunweihe <= updanRule[u.dan][2]:
            # 升段
            u.dan += 1
            u.timebeforeupdan = 0

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
        point1=sorteddict[0][1],
        point2=sorteddict[1][1],
        point3=sorteddict[2][1],
        point4=sorteddict[3][1],
        date=timezone.now(),
    )
    u1 = User.objects.get(qqnumber=battle.User1)
    u2 = User.objects.get(qqnumber=battle.User2)
    u3 = User.objects.get(qqnumber=battle.User3)
    u4 = User.objects.get(qqnumber=battle.User4)
    u1.firstplacetime += 1
    u2.secondplacetime += 1
    u3.thirdplacetime += 1
    u4.forthplacetime += 1
    avgrate = max((u1.rate+u2.rate+u3.rate+u4.rate)/4,1500)
    # Rate的变动 = 补正 * (对战结果 + (桌平均Rate-自己的Rate)/40)
    fix = 1-0.002*u1.alltime
    if fix<0.2:
        fix = 0.2
    u1.rate += fix * (30+(avgrate-u1.rate)/40)

    fix = 1-0.002*u2.alltime
    if fix<0.2:
        fix = 0.2
    u2.rate += fix * (10+(avgrate-u2.rate)/40)

    fix = 1-0.002*u3.alltime
    if fix<0.2:
        fix = 0.2
    u3.rate += fix * (-10+(avgrate-u3.rate)/40)

    fix = 1-0.002*u4.alltime
    if fix<0.2:
        fix = 0.2
    u4.rate += fix * (-30+(avgrate-u4.rate)/40)

    u1.alltime+=1
    u1.timebeforeupdan = min(u1.timebeforeupdan + 1, updanRule[u1.dan][0])
    checkUpDan(u1)

    u2.alltime+=1
    u2.timebeforeupdan = min(u2.timebeforeupdan + 1, updanRule[u2.dan][0])
    checkUpDan(u2)

    u3.alltime+=1
    u3.timebeforeupdan = min(u3.timebeforeupdan + 1, updanRule[u3.dan][0])
    checkUpDan(u3)

    u4.alltime+=1
    u4.timebeforeupdan = min(u4.timebeforeupdan + 1, updanRule[u4.dan][0])
    checkUpDan(u4)
    u1.save()
    u2.save()
    u3.save()
    u4.save()

    ret = "记录成功：\n" + \
            u1.Username + ": " + str(battle.point1) + "\n" + \
            u2.Username + ": " + str(battle.point2) + "\n" + \
            u3.Username + ": " + str(battle.point3) + "\n" + \
            u4.Username + ": " + str(battle.point4)
    return ret

def checkadduser(Users):
    for u in Users:
        try:
            isat = u[2]
            user = User.objects.get(qqnumber=u[0])
            if not isat:
                user.Username = u[1]
                user.save()
        except:
            user = User.objects.create(
                qqnumber=str(u[0]),
                Username=u[1],
                rate = 1500,

                firstplacetime = 0,
                secondplacetime = 0,
                thirdplacetime = 0,
                forthplacetime = 0,
                alltime = 0,

                timebeforeupdan = 0,

                dan = 0,
            )

def getuserinfo(qqnumber):
    try:
        user = User.objects.get(qqnumber=qqnumber)
        jinqishunwei = ""
        battles_dan = battles_show_name(user.qqnumber)[:min(10,user.alltime)]
        for b in battles_dan:
            if user.Username == b.User1:
                shunwei = 1
            if user.Username == b.User2:
                shunwei = 2
            if user.Username == b.User3:
                shunwei = 3
            if user.Username == b.User4:
                shunwei = 4
            jinqishunwei += str(shunwei)
        jinqishunwei = jinqishunwei[::-1]
        url = "http://shanghaitech-mahjong.top/userid/"+user.qqnumber
        msg = "昵称：{name}\n段位：{dan}\nrate：{rate}\n近期顺位：{jinqishunwei}\n更多数据请访问：{url}".format(
            name=user.Username,
            dan=dans[user.dan],
            rate=round(user.rate,2),
            jinqishunwei=jinqishunwei,
            url=url
        )
        return msg
    except:
        return "没有找到该用户的信息！"

def createyakuman(qqnumber,type,url):
    
    headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(url,headers=headers)
    with open("temp/tmp.jpg", mode = "wb") as f:
        f.write(r.content) #图片内容写入文件
    img_data = open("temp/tmp.jpg", 'rb')
    # img_file = File(img_data)
    # pic = Picture(name="test2022.jpg")
    # pic.path.save("test2022.jpg", img_file)
    yaku = yakuman.objects.create(qqnumber=qqnumber,
                                  yakuman_type=type,
                                  date=timezone.now())
    yaku.yakuman_photo.save("tmp.jpg", img_data)


def recordMajsoulbattle(paipu_url):
    import json, os
    
    cmd = "curl http://127.0.0.1:7236/paipu?uuid=" + paipu_url + " | jq > paipu.json"
    os.system(cmd)
    # 役种id：
    # 宝牌 31
    # 红宝牌 32
    # 里宝牌 33
    # 拔北宝牌 34
    dora_ids = [31,32,33,34]

    msg = """对战记录完成
    1位：{fstname} {fstpt}
    2位：{secname} {secpt}
    3位：{thdname} {thdpt}
    注：本场和牌中共计宝牌{doranum}枚，已记录。"""

    with open("paipu.json","r") as f:
        paipu = json.loads(f.read())
    uuid = paipu["head"]["uuid"]
    print(uuid)
    seats = [p["nickname"] for p in paipu["head"]["accounts"]]
    scores = []
    doranum = 0
    for p in paipu["head"]["result"]["players"]:
        nickname = seats[p["seat"]]
        scores.append([nickname, p["total_point"]/1000])
    for action in paipu["data"]["actions"]:
        if "result" in action.keys():
            if "data" in action["result"].keys():
                if "hules" in action["result"]["data"].keys():
                    for fan in action["result"]["data"]["hules"][0]["fans"]:
                        if fan["id"] in dora_ids:
                            doranum += fan["val"]

    msg = msg.format(
        fstname = scores[0][0],
        fstpt = scores[0][1],
        secname = scores[1][0],
        secpt = scores[1][1],
        thdname = scores[2][0],
        thdpt = scores[2][1],
        doranum = doranum
    )

    for s in scores:
        try:
            user = Majsouluser.objects.get(nickname=s[0])
            user.pt += s[1]
            user.save()
        except:
            user = Majsouluser.objects.create(
                nickname = s[0],
                pt = s[1]
            )

    b = Majsoulbattle.objects.create(
            User1 = scores[0][0],
            User2 = scores[1][0],
            User3 = scores[2][0],
            point1 = scores[0][1],
            point2 = scores[1][1],
            point3 = scores[2][1],
            date=timezone.now(),
            doranum=doranum,
            uuid=paipu_url)
    return msg

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


def rival(uid, oppouid):
    try:
        name = User.objects.get(qqnumber = uid).Username
        opponame = User.objects.get(qqnumber = oppouid).Username
        opponents = []
        msg = "您与{opponame}共进行过{alltime}场对局，你对TA的仇恨值为{rivalvalue}。\n你的胜率：{winrate}%\n你的均顺：{avgrank}\n对方均顺：{oppoavgrank}"
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
        for o in opponents:
            if o.Username == opponame:
                return msg.format(
                    opponame = opponame,
                    alltime = o.encountertime,
                    rivalvalue = o.rivalvalue,
                    winrate = round(o.winrate,2),
                    avgrank = round(o.selfavg,2),
                    oppoavgrank = round(o.oppoavg,2)
                )
        return "您未与{opponame}进行过对局。".format(opponame = opponame)
    except:
        return "未找到该用户的信息！"
# createyakuman("2461942798","大四喜","http://gchat.qpic.cn/gchatpic_new/2461942798/3879193066-2895620174-88159EBEAC341E6FD035DB13F155A10C/0?term=2&is_origin=0")
# print(getuserinfo("467091276"))
# print(recordbattle({"1001":30000,"1002":10000,"1003":50000,"1004":10000}))
