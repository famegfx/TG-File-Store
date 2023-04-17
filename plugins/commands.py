import os
import asyncio
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ListenerCanceled
from database.database import *
from config import *

BATCH = []


@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text("ᴘʀᴏᴄᴇꜱꜱᴇꜱɪɴɢ ...", quote=True)

    owner = await c.get_users(int(OWNER_ID))
    owner_username = owner.username if owner.username else 'Ns_bot_updates'

    # start text
    text = f"""ʜᴇʏ !{m.from_user.mention(style='md')}

 ɪ ᴀᴍ ᴘᴀɪɴꜱ  ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ

`ʏᴏᴜ ᴄᴀɴ ꜱᴛᴏʀᴇ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ꜰᴏʀ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ!`


ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ʙʏ: {owner.mention(style='md')}
"""

    # Buttons
    buttons = [
        [
            InlineKeyboardButton('ᴍʏ ꜰᴀᴛʜᴇʀ ', url=f"https://t.me/{owner_username}"),
            InlineKeyboardButton('ʜᴇʟᴘ', callback_data="help")
        ],
        [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ ', callback_data="about")
        ]
    ]

    # when button home is pressed
    if cb:
        return await m.message.edit(
                   text=text,
                   reply_markup=InlineKeyboardMarkup(buttons)
               )

    if len(m.command) > 1: # sending the stored file
        try:
            m.command[1] = await decode(m.command[1])
        except:
            pass

        if 'batch_' in m.command[1]:
            await send_msg.delete()
            cmd, chat_id, message = m.command[1].split('_')
            string = await c.get_messages(int(chat_id), int(message)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(message))

            if string.empty:
                owner = await c.get_users(int(OWNER_ID))
                return await m.reply_text(f"ꜱᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ꜰɪʟᴇ ᴡᴀꜱ ᴅᴇʟᴇᴛᴇᴅ ʙʏ ꜰɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\ɴ\ɴꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ {owner.mention(style='md')}")
            message_ids = (await decode(string.text)).split('-')
            for msg_id in message_ids:
                msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

                if msg.empty:
                    owner = await c.get_users(int(OWNER_ID))
                    return await m.reply_text(f"ꜱᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ꜰɪʟᴇ ᴡᴀꜱ ᴅᴇʟᴇᴛᴇᴅ ʙʏ ꜰɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\ɴ\ɴꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ {owner.mention(style='md')}")
                try:
                    await msg.copy(m.from_user.id, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(m.from_user.id, protect_content=PROTECT_CONTENT)
                except:
                    pass
            return

        chat_id, msg_id = m.command[1].split('_')
        msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            return await send_msg.edit(f"ꜱᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ꜰɪʟᴇ ᴡᴀꜱ ᴅᴇʟᴇᴛᴇᴅ ʙʏ ꜰɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\ɴ\ɴꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}\n\n\n" if msg.caption else ""
        as_uploadername = (await get_data(str(chat_id))).up_name
        
        if as_uploadername:
            if chat_id.startswith('-100'):
                channel = await c.get_chat(int(chat_id))
                caption += "__ᴜᴘʟᴏᴀᴅᴇʀ ᴅᴇᴛᴀɪʟꜱ:__\n\n" 
                caption += f"__ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇ :__ `{channel.title}`\n\n" 
                caption += f"__ᴜꜱᴇʀ ɴᴀᴍᴇ:__ @{channel.username}\n\n" if channel.username else "" 
                caption += f"__ᴄʜᴀɴɴᴇʟ ɪᴅ:__ `{channel.id}`\n\n" 
                caption += f"__ ᴅᴄ ɪᴅ:__ {channel.dc_id}\n\n" if channel.dc_id else "" 
                caption += f"__ᴍᴇᴍʙᴇʀꜱ ᴄᴏᴜɴᴛ:__ {channel.members_count}\n\n" if channel.members_count else ""
            else:
                user = await c.get_users(int(chat_id)) 
                caption += "__ᴜᴘʟᴏᴀᴅᴇʀ ᴅᴇᴛᴀɪʟꜱ:__\n\n" 
                caption += f"__ꜰɪʀꜱᴛ ɴᴀᴍᴇ :__ `{user.first_name}`\n\n" 
                caption += f"__ʟᴀꜱᴛ ɴᴀᴍᴇ:__ `{user.last_name}`\n\n" if user.last_name else "" 
                caption += f"__ᴜꜱᴇʀ ɴᴀᴍᴇ:__ @{user.username}\n\n" if user.username else "" 
                caption += f"__ ᴜꜱᴇʀ ɪᴅ:__ `{user.id}`\n\n" 
                caption += f"__ᴅᴄ ɪᴅ:__ {user.dc_id}\n\n" if user.dc_id else ""


        await send_msg.delete()
        await msg.copy(m.from_user.id, caption=caption, protect_content=PROTECT_CONTENT)


    else: # sending start message
        await send_msg.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_message(filters.command('me') & filters.incoming & filters.private)
async def me(c, m):
    """ ᴛʜɪꜱ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ ᴡʜᴇɴ /ᴍᴇ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀꜱ ᴜꜱᴇᴅ"""

    me = await c.get_users(m.from_user.id)
    text = "__ʏᴏᴜʀ ᴅᴇᴛᴀɪʟꜱ :__\n\n\n"
    text += f"__ꜰɪʀꜱᴛ ɴᴀᴍᴇ:__ `{me.first_name}`\n\n"
    text += f"__ʟᴀꜱᴛ ɴᴀᴍᴇ:__ `{me.last_name}`\n\n" if me.last_name else ""
    text += f"__ᴜꜱᴇʀ ɴᴀᴍᴇ:__ @{me.username}\n\n" if me.username else ""
    text += f"__ᴜꜱᴇʀ ɪᴅ:__ `{me.id}`\n\n"
    text += f"__ᴅᴄ ɪᴅ:__ {me.dc_id}\n\n" if me.dc_id else ""
    text += f"__ɪꜱ ᴠᴇʀɪꜰɪᴇᴅ ʙʏ ᴛᴇʟᴇɢʀᴀᴍ:__ `{me.is_verified}`\n\n" if me.is_verified else ""
    text += f"__ɪꜱ ꜰᴀᴋᴇ:__ {me.is_fake}\n\n" if me.is_fake else ""
    text += f"__ɪꜱ ꜱᴄᴀᴍ :__ {me.is_scam}\n\n" if me.is_scam else ""
    text += f"__ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ:__ {me.language_code}\n\n" if me.language_code else ""

    await m.reply_text(text, quote=True)


@Client.on_message(filters.command('batch') & filters.private & filters.incoming)
async def batch(c, m):
    """ This is for batch command"""
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    BATCH.append(m.from_user.id)
    files = []
    i = 1

    while m.from_user.id in BATCH:
        if i == 1:
            media = await c.ask(chat_id=m.from_user.id, text='ꜱᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ꜰɪʟᴇꜱ ᴏʀ ᴠɪᴅᴇᴏꜱ ᴏʀ ᴘʜᴏᴛᴏꜱ ᴏʀ ᴛᴇxᴛ ᴏʀ ᴀᴜᴅɪᴏ. ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ ꜱᴇɴᴅ /ᴄᴀɴᴄᴇʟ')
            if media.text == "/cancel":
                return await m.reply_text('ᴄᴀɴᴄᴇʟʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ')
            files.append(media)
        else:
            try:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('ᴅᴏɴᴇ', callback_data='done')]])
                media = await c.ask(chat_id=m.from_user.id, text='ᴅᴏɴᴇ ᴛᴏ ɢᴇᴛ ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ. ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ ꜱᴇɴᴅ /ᴄᴀɴᴄᴇʟ',  reply_markup=reply_markup)
                if media.text == "/cancel":
                    return await m.reply_text('ᴄᴀɴᴄᴇʟʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ')
                files.append(media)
            except ListenerCanceled:
                pass
            except Exception as e:
                print(e)
                await m.reply_text(text="ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
        i += 1

    message = await m.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ ")
    string = ""
    for file in files:
        if DB_CHANNEL_ID:
            copy_message = await file.copy(int(DB_CHANNEL_ID))
        else:
            copy_message = await file.copy(m.from_user.id)
        string += f"{copy_message.message_id}-"
        await asyncio.sleep(1)

    string_base64 = await encode_string(string[:-1])
    send = await c.send_message(m.from_user.id, string_base64) if not DB_CHANNEL_ID else await c.send_message(int(DB_CHANNEL_ID), string_base64)
    base64_string = await encode_string(f"batch_{m.chat.id}_{send.message_id}")
    bot = await c.get_me()
    url = f"https://t.me/{bot.username}?start={base64_string}"

    await message.edit(text=url)

@Client.on_message(filters.command('mode') & filters.incoming & filters.private)
async def set_mode(c,m):
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    usr = m.from_user.id
    if len(m.command) > 1:
        usr = m.command[1]
    caption_mode = (await get_data(usr)).up_name
    if caption_mode:
       await update_as_name(str(usr), False)
       text = "ᴜᴘʟᴏᴀᴅᴇʀ ᴅᴇᴛᴀɪʟꜱ ɪɴ ᴄᴀᴘᴛɪᴏɴ: ᴅɪꜱᴀʙʟᴇᴅ "
    else:
       await update_as_name(str(usr), True)
       text = "ᴜᴘʟᴏᴀᴅᴇʀ ᴅᴇᴛᴀɪʟꜱ ɪɴ ᴄᴀᴘᴛɪᴏɴ: ᴇɴᴀʙʟᴇᴅ "
    await m.reply_text(text, quote=True)

async def decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def encode_string(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
