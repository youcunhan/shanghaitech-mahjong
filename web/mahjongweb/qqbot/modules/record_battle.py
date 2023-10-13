# 本部分示例需使用 Saya 进行加载
import sys 
sys.path.append("..") 
from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Friend, Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from api import *
from mahjong301 import *
import random
channel = Channel.current()


from typing import Union
is_record_yakuman = False
yakuman_qqnum = None
yakuman_type = None
ptdict = {}
all_users = []
# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
# async def img(app: Ariadne, group: Group, message: MessageChain):
#     if message.display.strip() != "来张网上的涩图":
#         return
#     session = Ariadne.service.client_session
#     async with session.get("https://i1.hdslb.com/bfs/archive/5242750857121e05146d5d5b13a47a2a6dd36e98.jpg") as resp:
#         img_bytes = await resp.read()
#     await app.send_message(group, MessageChain(Image(data_bytes=img_bytes)))
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def hello(app: Ariadne, group: Group, member: Member, message: MessageChain):
    global is_record_yakuman, yakuman_type, yakuman_qqnum
    point = 1
    isat = False
    chosechaxun = False
    chooseyiman = False
    choosejichou = False
    selfqqnumber = str(member.id)
    if is_number(message.display) == False:
        if message[1].type == "Image" and is_record_yakuman:
            createyakuman(yakuman_qqnum,yakuman_type,message[1].url)
            is_record_yakuman = False
            await app.send_message(group, MessageChain("役满"+yakuman_type+"记录完成！"))
        if message.display == "!test" or message.display == "！test":
            await app.send_message(group, MessageChain(ptdict.__str__()))
            return
        if message.display == "!help" or message.display == "！帮助" or message.display == "!帮助" or message.display == "！help":
            await app.send_message(group, MessageChain("使用指南：http://shanghaitech-mahjong.top/help"))
            return
        if message.display == "！查询" or message.display == "！吃鱼" or message.display == "！被吃" or message.display == "！查查我的":
            qqnumber = str(member.id)
            msg = getuserinfo(qqnumber)
            await app.send_message(group, MessageChain(msg))
            return
        if message.display == "！注册" or message.display == "！改名":
            checkadduser([[str(member.id),member.name,False]])
            await app.send_message(group, MessageChain("玩家{name}注册成功！".format(name=member.name)))
            return
        if message.display == "！jrrp" or message.display == "!jrrp":
            easyyi = ["立直", "平和", "门前淸自摸和", "一杯口", "断幺九", "役牌", "对对和"]
            mediumyi = ["三色同顺", "一气通贯", "混全带幺九", "七对子", "混一色"]
            hardyi = ["三暗刻", "三杠子", "三色同刻", "混老头", "小三元", "纯全带幺九", "二杯口", "流局满贯", "清一色"]
            yiman = ["大三元", "小四喜", "大四喜", "字一色", "绿一色", "清老头", "国士无双", "四暗刻", "四暗刻单骑", "九莲宝灯", "纯正九莲宝灯", "四杠子"]
            rp = random.randint(0, 100)
            if rp<=10:
                rptype = "大凶"
                yi = random.choice(easyyi+["弃和"]+["弃和"]+["今日不宜打麻将~"])
            elif rp<=20:
                rptype = "凶"
                yi = random.choice(easyyi+easyyi+["弃和"]+["今日不宜打麻将~"])
            elif rp<=55:
                rptype = "吉"
                yi = random.choice(easyyi+mediumyi)
            elif rp<=80:
                rptype = "小吉"
                yi = random.choice(easyyi+easyyi+mediumyi+hardyi)
            elif rp<=90:
                rptype = "中吉"
                yi = random.choice(easyyi+mediumyi+hardyi+yiman)
            else:
                rptype = "大吉"
                yi = random.choice(hardyi+yiman+["买彩票去吧！"])

            msg = "今日人品：{rp}\n今日适宜役种：{yi}\n(为防止刷屏，一日内不可多次查询哦！)".format(
                rp = rptype,
                yi = yi
            )
            await app.send_message(group, MessageChain(msg))
            return
        if message.display == "取消":
            ptdict.clear()
            all_users.clear()
            await app.send_message(group, MessageChain("取消成功，请重新输入点数"))
            return
        if message.display[0] == "!" or message.display[0] == "！":
            if len(message.display.split(':', 1))==2:
                order, arg1 = message.display.split(':', 1)
                if order == "!雀魂牌谱" or order == "！雀魂牌谱":
                    url = arg1.strip()
                    url = url[url.index("=")+1:url.index("_")]
                    msg = recordMajsoulbattle(url)
                    await app.send_message(group, MessageChain(msg))
                    return
            if len(message.display.split(' ', 1))==2:
                order, arg1 = message.display.split(' ', 1)
                if order == "!记录牌谱" or order == "！记录牌谱":
                    msg = recordMajsoulbattle(arg1.strip())
                    await app.send_message(group, MessageChain(msg))
                    return
                if order == "!看看牌" or order == "！看看牌":
                    msg = kankanpai(arg1.strip(),"zh")
                    await app.send_message(group, MessageChain(msg))
                    return
                if order == "!役满" or order == "！役满":
                    is_record_yakuman = True
                    yakuman_qqnum = str(member.id)
                    yakuman_type = str(arg1)
                    return
                if order == "!匿名" or order == "！匿名":
                    username = "匿名用户"
                    isat = True
                    qqnumber = "0"
                    point = int(arg1)
        if len(message) <= 4:
        
            for msg in message:
                if msg.type == "At":
                    username = str(msg)
                    qqnumber = str(msg.target)
                    isat = True
                elif msg.type == "Plain":
                    text = msg.display.strip()
                    if is_number(text):
                        point = int(text)
                    elif text == "！查询" or text == "！吃鱼" or text == "！查查你的":
                        chosechaxun = True
                    elif text == "！记仇" or text == "!记仇" or text == "！仇恨值":
                        choosejichou = True
                    else:
                        if len(text.split(' ', 1))==2: 
                            order, arg1 = text.split(' ', 1)
                            if order == "!役满" or order == "！役满":
                                is_record_yakuman = True
                                chooseyiman = True
                                yakuman_type = str(arg1)
            if isat == False:
                return
    else:
        username = member.name
        qqnumber = str(member.id)
        point = int(message.display)
        isat = False
    if chosechaxun:
        msg = getuserinfo(qqnumber)
        await app.send_message(group, MessageChain(msg))
        return
    if choosejichou:
        msg = rival(selfqqnumber,qqnumber)
        await app.send_message(group, MessageChain(msg))
        return
    if chooseyiman:
        is_record_yakuman = True
        yakuman_qqnum = qqnumber
        return
    if point % 100!=0:
        return
    if qqnumber not in ptdict.keys():
        all_users.append([qqnumber,username,isat])
    ptdict[qqnumber] = point
    print(ptdict)
    print(all_users)
    if len(ptdict) == 4:
        sum = 0
        for value in ptdict.values():
            sum += value
        if sum != 100000:
            await app.send_message(group, MessageChain("点数有误，总和不为100000！"))
            return
        checkadduser(all_users)
        comment = recordbattle(ptdict)
        await app.send_message(group, MessageChain(comment))
        ptdict.clear()
        all_users.clear()
