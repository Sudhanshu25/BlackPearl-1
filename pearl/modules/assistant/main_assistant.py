from telethon import events, custom, Button
from telethon.tl.types import (
    Channel,
    Chat,
    User
)

import emoji
import asyncio
from googletrans import Translator
import re
import io
from math import ceil
from telethon import custom, events, Button
from pearl import CMD_LIST
from pearl.utils import pearl_on_cmd, edit_or_reply, sudo_cmd
from telethon.utils import get_display_name
from pearl.utils import pearl_on_cmd, sudo_cmd
from pearl.Configs import Config
from telethon import events
from datetime import datetime
from pearl.utils import pearl_on_cmd, edit_or_reply, sudo_cmd
import time
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from pearl import Lastupdate, bot
from pearl.modules.sql_helper.botusers_sql import add_me_in_db, his_userid
from pearl.modules.sql_helper.idadder_sql import add_usersid_in_db, get_all_users, already_added
from pearl.modules.sql_helper.blacklist_assistant import add_nibba_in_db, get_all_nibba, is_he_added, removenibba

@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    starttext = (f"Hello, {firstname} ! Nice To Meet You, Well I Am {bot_id}, An Powerfull Assistant Bot. \n\nMy [➤ Master](tg://user?id={bot.uid}) \nYou Can Talk/Contact My Master Using This Bot. \n\nIf You Want Your Own Assistant You Can Deploy From Button Below. \n\nPowered By [Black Pearl](t.me/pearlsupport)")
    if event.sender_id == bot.uid:
        await tgbot.send_message(
           vent,
           message=f"Hi Master, It's Me {bot_id}, Your Assistant ! \nWhat You Wanna Do today ?",
           buttons = [
           [custom.Button.inline("Show Users 🔥", data="users")],
           [custom.Button.inline("Commands For Assistant", data="gibcmd")],
           [Button.url("Add Me to Group 👥", f"t.me/{bot_username}?startgroup=true")]
            ]
           )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(
                event.sender_id
             )
        await tgbot.send_message(
           event.chat_id,
           message=starttext,
           link_preview=False,
           buttons = [
           [custom.Button.inline("Deploy your Black Pearl ", data="deploy")],
           [Button.url("Help Me ❓", "t.me/pearlsupport")]
       ]
      )


# Data's

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
        await event.delete()
        if event.query.user_id is not bot.uid:
            await tgbot.send_message(
                event.chat_id,
                message="You Can Deploy black Pearl In Heroku By Following Steps Bellow, You Can See Some Quick Guides On Support Channel Or On Your Own Assistant Bot. \nThank You For Contacting Me.",
                buttons = [
                [Button.url("Deploy Tutorial 📺", "https://youtu.be/xfHcm_e92eQ")],
                [Button.url("Need Help ❓", "t.me/pearlsupport")]
                 ]
                )



@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
        if event.query.user_id == bot.uid:
             await event.delete()
             total_users = get_all_users()
             users_list = "List Of Total Users In Bot. \n\n"
             for starked in total_users:
                 users_list += ("==> {} \n").format(int(starked.chat_id))
             with io.BytesIO(str.encode(users_list)) as tedt_file:
                 tedt_file.name = "userlist.txt"
                 await tgbot.send_file(
                     event.chat_id,
                     tedt_file,
                     force_document=True,
                     caption="Total Users In Your Bot.",
                     allow_cache=False
                     )
        else:
            pass
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
         await event.delete()
         grabon = "Hello Here Are Some Commands \n➤ /start - Check if I am Alive \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Sends Message To all Users In Bot \n➤ /id - Shows ID of User And Media. \n➤ /addnote - Add Note \n➤ /notes - Shows Notes \n➤ /rmnote - Remove Note \n➤ /alive - Am I Alive? \n➤ /bun - Works In Group , Bans A User. \n➤ /unbun - Unbans A User in Group \n➤ /prumote - Promotes A User \n➤ /demute - Demotes A User \n➤ /pin - Pins A Message \n➤ /stats - Shows Total Users In Bot"
         await tgbot.send_message(
             event.chat_id,
             grabon
         )
             

# Bot Permit.
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def all_messages_catcher(event):
    if is_he_added(event.sender_id):
        return
    if event.raw_text.startswith("/"):
        pass
    elif event.sender_id == bot.uid:
        return
    else:
        sender = await event.get_sender()
        chat_id = event.chat_id
        sed = await event.forward_to(bot.uid)
# Add User To Database ,Later For Broadcast Purpose
# (C) @SpecHide
        add_me_in_db(
            sed.id,
            event.sender_id,
            event.id
        )



@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def sed(event):
    msg = await event.get_reply_message()
    if msg is None:
        return
    real_nigga = msg.id
    msg_s = event.raw_text
    user_id, reply_message_id = his_userid(
        msg.id
        )
    if event.sender_id == bot.uid:
        if event.raw_text.startswith("/"):
            pass
        else:
            await tgbot.send_message(
            user_id,
            msg_s
            )

# broadcast
@tgbot.on(events.NewMessage(pattern="^/broadcast ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def sedlyfsir(event):
    msgtobroadcast = event.pattern_match.group(1)
    userstobc = get_all_users()
    error_count = 0
    sent_count = 0
    for starkcast in userstobc:
        try:
            sent_count += 1
            await tgbot.send_message(int(starkcast.chat_id), msgtobroadcast)
            await asyncio.sleep(0.2)
        except Exception as e:
            try:
                 logger.info(f"Error : {error_count}\nError : {e} \nUsers : {chat_id}"
                 )
            except:
                 pass
    await tgbot.send_message(
        event.chat_id,
        f"Broadcast Done in {sent_count} Group/Users and I got {error_count} Error and Total Number Was {len(userstobc)}"
        )


@tgbot.on(events.NewMessage(pattern="^/stats ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    starkisnoob = get_all_users()
    await event.reply(f"**Stats Of Your Bot** \nTotal Users In Bot => {len(starkisnoob)}")
    
@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    grabonx = "Hello Here Are Some Commands \n➤ /start - Check if I am Alive \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Sends Message To all Users In Bot \n➤ /id - Shows ID of User And Media. \n➤ /addnote - Add Note \n➤ /notes - Shows Notes \n➤ /rmnote - Remove Note \n➤ /alive - Am I Alive? \n➤ /bun - Works In Group , Bans A User. \n➤ /unbun - Unbans A User in Group \n➤ /prumote - Promotes A User \n➤ /demute - Demotes A User \n➤ /pin - Pins A Message \n➤ /stats - Shows Total Users In Bot"
    await event.reply(grabonx)
    
@tgbot.on(events.NewMessage(pattern="^/block ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        real_nigga = msg.id
        msg_s = event.raw_text
        user_id, reply_message_id = his_userid(
        msg.id
        )
    if is_he_added(user_id):
        await event.reply("Already Blacklisted")
    elif not is_he_added(user_id):
        add_nibba_in_db(
            user_id
          )
        await event.reply("Blacklisted This Dumb Person")
        await tgbot.send_message(user_id, "You Have Been Blacklisted And You Can't Message My Master Now.")

@tgbot.on(events.NewMessage(pattern="^/unblock ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        real_nigga = msg.id
        msg_s = event.raw_text
        user_id, reply_message_id = his_userid(
        msg.id
        )
    if not is_he_added(user_id):
        await event.reply("Not Even. Blacklisted 🤦🚶")
    elif is_he_added(user_id):
        removenibba(
            user_id
          )
        await event.reply("DisBlacklisted This Dumb Person")
        await tgbot.send_message(user_id, "Congo! You Have Been Unblacklisted By My Master.")
