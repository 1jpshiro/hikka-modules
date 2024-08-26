#              © Copyright 2024
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: 猫ちゃん(@shiro_hikka)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio

class StickerStealer(loader.Module):
    """Emoji/sticker stealer"""

    strings = {
        "name": "StickerStealer",
        "incorrect": "<emoji document_id=5231302159739395058>🔒</emoji> <i>It's not a sticker or emoji</i>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "emoji",
                "emsaved",
                lambda: "Specify a name of your emoji pack",
            ),
            loader.ConfigValue(
                "vs",
                "vssaved",
                lambda: "Specify a name if your video sticker pack"
            ),
            loader.ConfigValue(
                "ss",
                "sssaved",
                lambda: "Specify a name of your static sticker pack"
            )
        )

    def checkType(self, reply, message):
        if hasattr(reply, "media"):
            if hasattr(reply.media, "document"):
                if hasattr(reply.media.document, "attributes"):
                    if len(reply.media.document.attributes) > 1:
                        if hasattr(reply.media.document.attributes[1], "stickerset"):
                            if hasattr(reply.media.document.attributes[0], "duration"):
                                return 3
                            else:
                                return 4

        if not (reply.entities is None):
            return 1

        if hasattr(message, "reply_to"):
            if not (message.reply_to.quote_entities is None):
                return 2

        else:
            return 0

    async def stealcmd(self, message: Message):
        """ <reply / quote reply> - add an emoji or sticker to your pack\nEmoji: only one type of emoji at time is available"""
        await utils.answer(message, "<i>....</i>")
        reply = await message.get_reply_message()
        bot = "Stickers"

        dict_cfg = {
            1: self.config["emoji"],
            2: self.config["emoji"],
            3: self.config["vs"],
            4: self.config["ss"]
        }

        dict_type = {
            1: "An emoji",
            2: "An emoji",
            3: "A sticker",
            4: "A sticker"
        }

        async with self.client.conversation(bot) as bot:
            send = await bot.send_message("/addsticker")
            resp = await bot.get_response()

            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            _type = self.checkType(reply, message)

            match _type:
                case 1 | 2:
                    send = await bot.send_message(self.config['emoji'])
                case 3:
                    send = await bot.send_message(self.config['vs'])
                case 4:
                    send = await bot.send_message(self.config['ss'])
                case _:
                    await utils.answer(
                        message,
                        self.strings["incorrect"]
                    )

                    resp = await bot.get_response()
                    await resp.delete()
                    return

            resp = await bot.get_response()
            if resp.text == "Не выбран набор стикеров.":
                await utils.answer(
                    message,
                    f"<i>Create {dict_type[a].lower()} pack with public name</i> <b>{dict_cfg[a]}</b>"
                )
                await resp.delete()
                await send.delete()
                return

            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            match _type:
                case 1:
                    emoji = reply.message
                    toSend = reply
                case 2:
                    rep = message.reply_to
                    emoji = rep.quote_text
                    qoute_rep = rep.quote_entities[0].document_id
                    toSend = f"<emoji document_id={quote_rep}>{emoji}</emoji>"
                case _:
                    emoji = reply.media.document.attributes[1].alt
                    toSend = reply

            send = await bot.send_message(toSend)
            resp = await bot.get_response()
            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            send = await bot.send_message(emoji)
            resp = await bot.get_response()
            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            await utils.answer(
                message,
                f"<b>{dict_type[a]} has been added</b>"
            )