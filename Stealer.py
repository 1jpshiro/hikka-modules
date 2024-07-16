#              © Copyright 2024
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: 猫ちゃん

from .. import loader, utils
from telethon.tl.types import Message
import asyncio

class Stealer(loader.Module):
    """Emoji/sticker stealer"""

    strings = {
        "name": "Stealer",
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
        _dict = {
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

            a = self.checkType(reply, message)
            if any(a == i for i in [1, 2]):
                send = await bot.send_message(self.config['emoji'])
            elif a == 3:
                send = await bot.send_message(self.config['vs'])
            elif a == 4:
                send = await bot.send_message(self.config['ss'])
            else:
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
                    f"<i>Create {_dict[a].lower()} pack with public name</i> <b>{dict_cfg[a]}</b>"
                )
                await resp.delete()
                await send.delete()
                return
            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            if a == 1:
                t = reply.message
                _send = reply
            elif a == 2:
                tt = message.reply_to
                t = tt.quote_text
                t_ = tt.quote_entities[0].document_id
                _send = f"<emoji document_id={t_}>{t}</emoji>"
            else:
                t = reply.media.document.attributes[1].alt
                _send = reply

            send = await bot.send_message(_send)
            resp = await bot.get_response()
            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            send = await bot.send_message(t)
            resp = await bot.get_response()
            await asyncio.sleep(1)
            await send.delete()
            await resp.delete()

            await utils.answer(
                message,
                f"<b>{_dict[a]} has been added</b>"
            )
