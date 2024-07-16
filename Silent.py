#              © Copyright 2024
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: 猫ちゃん

from .. import loader, utils
from telethon.tl.types import Message
import asyncio

class Silent(loader.Module):
    """Mutes tags"""

    strings = {
        "name": "Silent",
        "tag_mentioned": "<b>🤫 Silent is active</b>",
        "stags_status": "<b>🤫 Silent is {} now</b>",
        "cfg": "Should not write a message about the Silent works?"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "silent",
                True,
                lambda: self.strings["cfg"],
                validator = loader.validators.Boolean()
            )
        )

    async def stagscmd(self, message: Message):
        """ <on/off> - toggle afk mode"""
        args = utils.get_args_raw(message)

        if args not in ["on", "off"]:
            await utils.answer(
                message,
                self.strings["stags_status"].format(
                    "active" if self.get("stags", False) else "inactive"
                ),
            )
            return

        args = args == "on"
        self.set("stags", args)
        await utils.answer(
            message,
            self.strings["stags_status"].format("now on" if args else "now off"),
        )
        await asyncio.sleep(4)
        await message.delete()

    async def watcher(self, message: Message):
        if (
            not getattr(message, "mentioned", False)
            or not self.get("stags", False)
        ):
            return

        await self._client.send_read_acknowledge(
            message.chat_id,
            clear_mentions=True,
        )

        if not self.config["silent"]:
            ms = await utils.answer(message, self.strings("tag_mentioned"))
            await asyncio.sleep(2)
            await ms.delete()
