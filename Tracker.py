from .. import loader, utils
from telethon.tl.types import Message
from ..inline.types import InlineCall
import datetime

class Tracker(loader.Module):

    strings = {
        "name": "Tracker",
        "enabled": "The tracker was succesfully enabled",
        "disabled": "Thr tracker was succesfully disabled",
        "no_user": "Seems this user does not exist, try another ID/Username",
        "change_status": "You just changed a status of tracking the user",
        "new_user": "You've succesfully added new user to track",
        "no_stat": "You're currently tracking no user"
    }

    async def client_ready(self, client, db):
        if self.db.get(__name__, "status") is None:
            self.db.set(__name__, "status", False)
        if self.db.get(__name__, "users") is None:
            self.db.set(__name__, "users", {})

    async def statStatus(self, call: InlineCall, ID) -> None:
        users = self.db.get(__name__, "users")
        users[ID]["active"] = not(users[ID]["active"])
        self.db.set(__name__, "users", users)
        await call.answer(self.strings["change_status"])

    async def showStat(self, call: InlineCall, ID, action) -> None:
        users = self.db.get(__name__, "users")
        ID = ID+1 if action == "next" else ID-1
        user = await self.client.get_entity(users[ID]["user_id"])

        match users[ID]["active"]:
            case True:
                status = "In process"
            case False:
                status = "Inactive"

        text = (
            f"<b>ID:</b> <a href='tg://user?id={user.id}'>{user.id}</a>\n"+
            "\n"+
            f"      <b>Nicknames</b>\n"+
            "\n".join(users[ID]["nicks"])+
            "\n"+
            "        <b>Usernames</b>\n"+
            "\n".join(users[ID]["unames"])
        )

        await call.edit(
            text=text,
            reply_markup=[
                [
                    {
                        "text": f"Tracking status: {status}",
                        "callback": self.statStatus(ID)
                    }
                ],
                [
                    {
                        "text": "Previous user",
                        "callback": self.showStat(ID, "prev")
                    },
                    {
                        "text": "Next user",
                        "callback": self.showStat(ID, "next")
                    }
                ]
            ]
        )

    async def trackcmd(self, message: Message):
        isEnDis = not(self.db.get(__name__, "status") is True)
        self.db.set(__name__, "status")
        match isEnDis:
            case True:
                await utils.answer(message, self.strings["enabled"])
            case False:
                await utils.answer(message, self.strings["disabled"])

    async def addtrackcmd(self, message: Message):
        args = utils.get_args_raw(message)
        try:
            user = await self.client.get_entity(int(args) if args.isdigit() else args)
        except:
            await utils.answer(message, self.strings["no_user"])
            return

        users = self.db.get(__name__, "users")
        ID = int(len(users)+1)
        UID = user.id

        users[ID] = {}

        users[ID]["nicks"] = [f"      {user.first_name+' '}{user.last_name if user.last_name else ''}"]
        users[ID]["unames"] = [f"      {'@'+user.username if user.username else '<i>Empty</i>'}"]
        users[ID]["active"] = True
        users[ID]["user_id"] = UID

        self.db.set(__name__, "users", users)
        await utils.answer(message, self.strings["new_user"])

    async def trackstatcmd(self, message: Message):
        users = self.db.get(__name__, "users")
        if len(users) == 0:
            await utils.answer(message, self.strings["no_stat"])
            return

        ID = 1
        user = await self.client.get_entity(users[ID]["user_id"])

        match users[ID]["active"]:
            case True:
                status = "In process"
            case False:
                status = "Inactive"

        text = (
            f"<b>ID:</b> <a href='tg://user?id={user.id}'>{user.id}</a>\n"+
            "\n"+
            f"      <b>Nicknames</b>\n"+
            "\n".join(users[ID]["nicks"])+
            "\n"+
            "        <b>Usernames</b>\n"+
            "\n".join(users[ID]["unames"])
        )

        await self.inline.form(
            text=text,
            message=message,
            reply_markup=[
                [
                    {
                        "text": f"Tracking status: {status}",
                        "callback": self.statStatus(ID)
                    }
                ],
                [
                    {
                        "text": "Previous user",
                        "callback": self.showStat(ID, "prev")
                    },
                    {
                        "text": "Next user",
                        "callback": self.showStat(ID, "next")
                    }
                ]
            ]
        )

    async def watcher(self, message: Message):
        users = self.db.get(__name__, "users")
        if len(users) == 0:
            return

        for i in users:
            if users[i]["active"] is False:
                continue
            entity = await self.client.get_entity(i["user_id"])
            nick = f"      {entity.first_name+' '}{entity.last_name if entity.last_name else ''}"
            username = entity.username if entity.username else '<i>Empty</i>'
            time = datetime.datetime.now()
            date = str(time.date()).split('-')
            hms = str(time.time()).split(':')

            if nick != users[i]["nicks"][-1]:
                users[i]["nicks"].append("[{}.{}.{} - {}:{}:{}] {}".format(
                    date[2],
                    date[1],
                    date[0],
                    hms[0],
                    hms[1],
                    hms[2].split('.')[0],
                    nick
                ))

            if username != users[i]["unames"][-1]:
                users[i]["unames"].append("[{}.{}.{} - {}:{}:{}] {}".format(
                    date[2],
                    date[1],
                    date[0],
                    hms[0],
                    hms[1],
                    hms[2].split(',')[0],
                    f"      @{username}"
                ))

            self.db.set(__name__, "users", users)
            await asyncio.sleep(1800)