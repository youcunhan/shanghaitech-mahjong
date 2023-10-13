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

channel = Channel.current()


from typing import Union

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
    if is_number(message.display) == False:
        if message.display == "取消":
            ptdict.clear()
            all_users.clear()
            await app.send_message(group, MessageChain("取消成功，请重新输入点数"))
        return
    point = int(message.display)
    username = member.name
    qqnumber = member.id
    if username not in ptdict.keys():
        all_users.append([qqnumber,username])
    ptdict[username] = point
    print(ptdict)
    print(all_users)
    if len(ptdict) == 4:
        sum = 0
        for value in ptdict.values():
            sum += value
        if sum != 100000:
            await app.send_message(group, MessageChain("点数有误，总和不为100000！"))
            return
        added = checkadduser(all_users)
        if len(added) != 0:
            usertext = ",".join(added)
            await app.send_message(group, MessageChain("新用户"+usertext+"已添加！"))
        recordbattle(ptdict)
        await app.send_message(group, MessageChain("记录完成："+ptdict.__str__()))
        ptdict.clear()
        all_users.clear()