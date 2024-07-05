# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
from pyrogram import filters, Client, enums
from plugins.database import unpack_new_file_id
from clone_plugins.users_api import get_user, get_short_link
import base64

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
from pyrogram import filters, Client, enums
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid, UsernameNotModified
from config import ADMINS, LOG_CHANNEL, FILE_STORE_CHANNEL, BOT_USERNAME
from plugins.database import unpack_new_file_id

import re
import os
import json
import base64
import logging

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
import re
import json
import os
import base64
from pyrogram import Client, filters
from pyrogram.errors import ChannelInvalid, UsernameInvalid, UsernameNotModified

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@Client.on_message(filters.command(['batch', 'pbatch']))
async def gen_link_batch(bot, message):
    logger.info("Command received: %s", message.text)

    if " " not in message.text:
        await message.reply("Use correct format.\nExample /batch https://t.me/vj_botz/10 https://t.me/vj_botz/20.")
        logger.warning("Incorrect format: space not found in message text")
        return

    links = message.text.strip().split(" ")
    if len(links) != 3:
        await message.reply("Use correct format.\nExample /batch https://t.me/vj_botz/10 https://t.me/vj_botz/20.")
        logger.warning("Incorrect format: expected 3 parts, got %d", len(links))
        return

    cmd, first, last = links
    regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")

    match = regex.match(first)
    if not match:
        await message.reply('Invalid link')
        logger.error("Invalid link: %s", first)
        return

    f_chat_id = match.group(4)
    f_msg_id = int(match.group(5))
    if f_chat_id.isnumeric():
        f_chat_id = int("-100" + f_chat_id)
    logger.info("Parsed first link: chat_id=%s, msg_id=%d", f_chat_id, f_msg_id)

    match = regex.match(last)
    if not match:
        await message.reply('Invalid link')
        logger.error("Invalid link: %s", last)
        return

    l_chat_id = match.group(4)
    l_msg_id = int(match.group(5))
    if l_chat_id.isnumeric():
        l_chat_id = int("-100" + l_chat_id)
    logger.info("Parsed last link: chat_id=%s, msg_id=%d", l_chat_id, l_msg_id)

    if f_chat_id != l_chat_id:
        await message.reply("Chat ids not matched.")
        logger.error("Chat IDs do not match: %s vs %s", f_chat_id, l_chat_id)
        return

    try:
        chat_id = (await bot.get_chat(f_chat_id)).id
    except ChannelInvalid:
        await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
        logger.exception("Channel invalid")
        return
    except (UsernameInvalid, UsernameNotModified):
        await message.reply('Invalid Link specified.')
        logger.exception("Username invalid or not modified")
        return
    except Exception as e:
        await message.reply(f'Errors - {e}')
        logger.exception("Exception occurred while getting chat ID")
        return

    logger.info("Chat ID retrieved: %d", chat_id)

    sts = await message.reply("**ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋ ғᴏʀ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ**.\n**ᴛʜɪs ᴍᴀʏ ᴛᴀᴋᴇ ᴛɪᴍᴇ ᴅᴇᴘᴇɴᴅɪɴɢ ᴜᴘᴏɴ ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs**")

    if chat_id in FILE_STORE_CHANNEL:
        string = f"{f_msg_id}_{l_msg_id}_{chat_id}_{cmd.lower().strip()}"
        b_64 = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
        user_id = message.from_user.id
        user = await get_user(user_id)
        bot_username = (await client.get_me()).username
        share_link = f"https://t.me/{bot_username}?start=DSTORE-{b_64}"
        await sts.edit(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>")
        short_link = await get_short_link(user, share_link)
        await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {short_link}</b>")
        return

    FRMT = "**ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋ...**\n**ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs:** {total}\n**ᴅᴏɴᴇ:** {current}\n**ʀᴇᴍᴀɪɴɪɴɢ:** {rem}\n**sᴛᴀᴛᴜs:** {sts}"

    outlist = []
    og_msg = 0
    tot = 0
    async for msg in bot.iter_messages(f_chat_id, l_msg_id, f_msg_id):
        tot += 1
        if msg.empty or msg.service:
            continue
        if not msg.media:
            continue
        try:
            file_type = msg.media
            file = getattr(msg, file_type.value)
            caption = getattr(msg, 'caption', '')
            if caption:
                caption = caption.html
            if file:
                file = {
                    "file_id": file.file_id,
                    "caption": caption,
                    "title": getattr(file, "file_name", ""),
                    "size": file.file_size,
                    "protect": cmd.lower().strip() == "/pbatch",
                }
                og_msg += 1
                outlist.append(file)
        except Exception as e:
            logger.exception("Exception occurred while processing messages")
            pass

        if not og_msg % 20:
            try:
                await sts.edit(FRMT.format(total=l_msg_id-f_msg_id, current=tot, rem=((l_msg_id-f_msg_id) - tot), sts="Saving Messages"))
            except Exception as e:
                logger.exception("Exception occurred while updating status message")
                pass

    with open(f"batchmode_{message.from_user.id}.json", "w+") as out:
        json.dump(outlist, out)
        logger.info("File batchmode_%d.json created", message.from_user.id)

    post = await bot.send_document(LOG_CHANNEL, f"batchmode_{message.from_user.id}.json", file_name="Batch.json", caption="⚠️Generated for filestore.")
    os.remove(f"batchmode_{message.from_user.id}.json")
    logger.info("File batchmode_%d.json sent to LOG_CHANNEL and removed locally", message.from_user.id)

    file_id, ref = unpack_new_file_id(post.document.file_id)
    user_id = message.from_user.id
    user = await get_user(user_id)
    bot_username = (await client.get_me()).username
    share_link = f"https://t.me/{bot_username}?start=BATCH-{file_id}"
    await sts.edit(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\nContains `{og_msg}` files.\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>")
    short_link = await get_short_link(user, share_link)
    await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {short_link}</b>")
   
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command(['link', 'plink']))
async def gen_link_s(client: Client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')
    file_type = replied.media
    if file_type not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
        return await message.reply("Reply to a supported media")
    if message.has_protected_content:
        return await message.reply("okDa")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    file_id, ref = unpack_new_file_id((getattr(replied, file_type.value)).file_id)
    string = 'filep_' if message.text.lower().strip() == "/plink" else 'file_'
    string += file_id
    outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    user_id = message.from_user.id
    user = await get_user(user_id)
    # Get the bot's username
    bot_username = (await client.get_me()).username
    share_link = f"https://t.me/{bot_username}?start={outstr}"
    await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>")
    short_link = await get_short_link(user, share_link)
    await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {short_link}</b>")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
