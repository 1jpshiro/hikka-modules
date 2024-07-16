# meta developer: 猫ちゃん

from telethon.tl.types import Message
from .. import loader, utils

class pmstat(loader.Module):
    """Counting how many messages did you and your chat partner write"""

    strings = {
        "name": "PMstat",
        "q": "<emoji document_id=5444965061749644170>👨‍💻</emoji> <i>All in all, {} messages were counted from</i> <b>{}</b>",
        "pm": "<i>Use in PM only</i>"
    }

    async def statcmd(self, message: Message):
        """ [-p] [-s] - (-p - counts your chat partner messages) (-s - send result to the saved messages)"""
        args = utils.get_args_raw(message)
        if not message.is_private:
            await utils.answer(message, self.strings['pm'])
            return

        await message.delete()
        chat = await self.client.get_entity(message.peer_id.user_id)
        w = "you" if "-p" not in args else f"<a href='tg://user?id={chat.id}'>{chat.first_name}</a>"
        s = chat.id if "-s" not in args else self.tg_id
        r = 0
        _r = []

        async for j in self.client.iter_messages(chat.id):
            _r.append(j)

        if "-p" in args:
            for l in _r:
                if l.from_id != self.tg_id:
                    r += 1
        else:
            for p in _r:
                if p.from_id == self.tg_id:
                    r += 1

        await message.client.send_message(
            s,
            self.strings['q'].format(r, w)
        )
