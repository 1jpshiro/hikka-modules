#              © Copyright 2024
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: 猫ちゃん(@shiro_hikka)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio

class DelMyMsgs(loader.Module):
    """Delete all your messages in current chat"""

    strings = {
        "name": "DelMyMsgs"
    }

    async def purgecmd(self, message: Message):
        """ [reply] - delete all your messages in current chat or only ones up to message you replyed to"""
        reply = await message.get_reply_message()
        is_last = False

        async for i in self.client.iter_messages(message.chat.id):
            if i.from_id == self.tg_id:
                if reply:
                    if is_last:
                        break
                    if i.id == reply.id:
                        is_last = True
                await message.client.delete_messages(message.chat.id, [i.id])

        q = await utils.answer(message, "<b>Done</b>")
        await asyncio.sleep(2)
        await q.delete()