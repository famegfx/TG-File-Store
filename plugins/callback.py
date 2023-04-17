import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .commands import start, BATCH
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ?? **

★ ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ꜰɪʟᴇꜱ ɪ ᴡɪʟʟ ꜱᴛᴏʀᴇ ꜰɪʟᴇ ᴀɴᴅ ɢɪᴠᴇ ʏᴏᴜ ꜱʜᴀʀᴇ ᴀʙʟᴇ ʟɪɴᴋ


**ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ɪɴ ᴄʜᴀɴɴᴇʟ ᴛᴏᴏ**

★ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴡɪᴛʜ ᴇᴅɪᴛ ᴘᴇʀᴍɪꜱꜱɪᴏɴ. ᴛʜᴀᴛꜱ ᴇɴᴏᴜɢʜ ɴᴏᴡ ᴄᴏɴᴛɪɴᴜᴇ ᴜᴘʟᴏᴀᴅɪɴɢ ꜰɪʟᴇꜱ ɪɴ ᴄʜᴀɴɴᴇʟ ɪ ᴡɪʟʟ ᴇᴅɪᴛ ᴀʟʟ ᴘᴏꜱᴛꜱ ᴀɴᴅ ᴀᴅᴅ ꜱʜᴀʀᴇ ᴀʙʟᴇ ʟɪɴᴋ ᴜʀʟ ʙᴜᴛᴛᴏɴꜱ

**ʜᴏᴡ ᴛᴏ ᴇɴᴀʙʟᴇ ᴜᴘʟᴏᴀᴅᴇʀ ᴅᴇᴛᴀɪʟꜱ ɪɴ ᴄᴀᴘᴛɪᴏɴ**

★ ★ ᴜꜱᴇ /ᴍᴏᴅᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ᴀɴᴅ ᴀʟꜱᴏ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ `/ᴍᴏᴅᴇ ᴄʜᴀɴɴᴇʟ_ɪᴅ` ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴄᴀᴘᴛɪᴏɴ ꜰᴏʀ ᴄʜᴀɴɴᴇʟ ᴍꜱɢ."""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='home'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ ', callback_data='about')
        ],
        [
            InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""--**ᴍʏ ᴅᴇᴛᴀɪʟꜱ :**--

ᴍʏ ɴᴀᴍᴇ : {bot.mention(style='md')}
    
ʟᴀɴɢᴜᴀɢᴇ : [Python 3](https://www.python.org/)

ꜰʀᴀᴍᴇᴡᴏʀᴋ : [Pyrogram](https://github.com/pyrogram/pyrogram)

ᴅᴇᴠʟᴏᴘᴇʀ : {owner.mention(style='md')}

ᴄʜᴀɴɴᴇʟ : [ᴘᴀɪɴ ʙᴏᴛ ᴜᴘᴅᴀᴛᴇ](https://t.me/Ns_bot_update)

ɢʀᴏᴜᴘ : [ᴘᴀɪɴ ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛ ](https://t.me/Ns_Bot_supporte)

ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : [ᴘʀᴇꜱꜱ ᴍᴇ](ᴀᴘɴɪ ᴍᴀᴀ ᴍᴀᴛ ᴄʜᴜᴅᴀ )
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('ʜᴏᴍᴇ ', callback_data='home'),
            InlineKeyboardButton('ʜᴇʟᴘ ', callback_data='help')
        ],
        [
            InlineKeyboardButton('ᴄʟᴏꜱᴇ ', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("ᴅᴇʟᴇᴛᴇᴅ ꜰɪʟᴇꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ")
