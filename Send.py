#              © Copyright 2024
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: 猫ちゃん

from .. import utils, loader
from telethon.tl.types import Message
import asyncio

class send(loader.Module):
    """Massively sending message to some kind of chat"""

    strings = {
        "name": "Massive sending"
    }

    async def sendToPm(self, send_list):
        async for i in self.client.iter_dialogs():
            entity = await self.client.get_entity(i.id)
            if hasattr(entity, "first_name"):
                send_list.append(i.id)

    async def sendToGroup(self, send_list):
        async for i in self.client.iter_dialogs():
            entity = await self.client.get_entity(i.id)
            if hasattr(entity, "broadcast"):
                if getattr(entity, "broadcast") is False:
                    send_list.append(i.id)
 
    async def sendToChannel(self, send_list):
        async for i in self.client.iter_dialogs():
            entity = await self.client.get_entity(i.id)
            if hasattr(entity, "broadcast"):
                if getattr(entity, "broadcast") is True:
                    send_list.append(i.id)

    async def sendToAll(self, send_list):
        async for i in self.client.iter_dialogs():
            send_list.append(i.id)


    async def sendcmd(self, message: Message):
        """ [pm / group / channel] <message> - start massive sending"""
        args = utils.get_args_raw(message)
        send_list = []
        err_count = 0
        text = args.split()[1] if args.split()[0] in ["pm", "group", "channel"] else args

        if not args:
            await utils.answer(message, "<i>Specify args</i>")
            return
	
        q = await utils.answer(message, "<i>Sending...</i>")

        if args.split()[0] == "pm":
            await self.sendToPm(send_list)
        elif args.split()[0] == "group":
            await self.sendToGroup(send_list)
        elif args.split()[0] == "channel":
            await self.sendToChannel(send_list)
        else:
            await self.sendToAll(send_list)

        for i in send_list:
            try:
                await message.client.send_message(i, text)
                await asyncio.sleep(2)
            except:
                err_count += 1
                continue

        await utils.answer(q, f"<i>Message has been sent</i>\n\n<i>Couldn't send message to <u>{err_counter}</u> chats</i>")
        send_list = []
        err_count = 0
