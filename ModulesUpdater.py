# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Auto modules updater
# Description: Suggest to get updated if your version isn't up-to-date
# Commands:
# ---------------------------------------------------------------------------------
#              © Copyright 2025
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# scope: hikka_only
# meta developer: @shiro_hikka
# meta banner: https://0x0.st/s/FIR0RnhUN5pZV5CZ6sNFEw/8KBz.jpg
# ---------------------------------------------------------------------------------

__version__ = (0, 0, 1)

from .. import loader, utils
from telethon.tl.types import Message
import re
import logging
import ast
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

@loader.tds
class ModulesUpdater(loader.Module):
    """Suggest to get updated if your version isn't up-to-date"""

    async def client_ready(self):
        path = self.db.get(__name__, "json")
        if not path:
            self.db.set(__name__, "json", {})


    async def watcher(self, message: Message):
        prefix = self.get_prefix()
        aliases = self.db.get("CoreMod", "aliases")
        aliases["help"] = "help"
        aliases["lm"] = "loadmod"
        aliases["dlm"] = "dlmod"
        messageSplit = message.text.split()
        messageSplit = [i for i in messageSplit() if i]

        url = "https://raw.githubusercontent.com/1jpshiro/hikka-modules/main/full.txt"
        full_txt = requests.get(url)
        if full_txt.status_code != 200:
            return

        modList = full_txt.text.splitlines()
        path = Path("~/Hikka/loaded_modules")
        abs_path = path.expanduser()
        loadedMods = [
            i for i in path.iterdir() if i.is_file()
        ]

        if loadedMods:
            any_exist = [
                i for i in modList
                for j in loadedMods
                if i == re.sub(r"_"+f"{self.tg_id}\.py", "", j)
            ]

        if any_exist:
            versionList = self.db.get(__name__, "json")
            for item in any_exist:
                if not versionList[item]:
                    file = open(f"abs_path/{item}.py", "r").read()
                    fileSplit = file.splitlines()
                    verLine = [
                        line for line in fileSplit if re.search(r"__version__.*=.*\(.*\)", line)
                    ]
                    currentVersion = re.sub(r"__version__.*\=", "", verLine[0]).strip()
                    versionList[item] = ast.literal_eval(currentVersion)
            self.db.set(__name__, "json", versionList)

        if len(messageSplit) < 2:
            return

        if not messageSplit[0].startswith(prefix):
            return

        if any(
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "help"
        ) or (
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "help"
            )
        ):
            if messageSplit[0] == prefix:
                messageSplit.pop(1)

            messageSplit.pop(0)

            for mod in modList:
                if messageSplit[0].lower() == mod.lower():
                    mod_link = f"https://raw.githubusercontent.com/1jpshiro/hikka-modules/main/{mod}.py"
                    mod_name = mod
                    break

            response = requests.get(mod_link)
            if response.status_code != 200:
                return

            modSplit = response.text.splitlines()
            version = [
                line for line in modSplit if re.search(r"__version__.*\=.*\(.*\)", line)
            ]
            version = re.sub(r"__version__.*\=", "", version[0]).strip()
            version = ast.literal_eval(version)

            if not mod_name in loadedMods:
                return

            currentVersion = self.db.get(__name__, "json")[mod_name]

            proceed = True if (
                version[0] > currentVersion[0]
            ) or (
                version[1] > currentVersion[1]
                and version[0] == currentVersion[0]
            ) or (
                version[2] > currentVersion[2]
                and version[1] == currentVersion[1]
                and version[0] == currentVersion[0]
            ) else False


        if (
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "dlmod"
        ) or (
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "dlmod"
            )
        ):
            if messageSplit[0] == prefix:
                messageSplit.pop(1)

            messageSplit.pop(0)

            for mod in modList:
                if (
                    mesageSplit[0].split('/')[-1].lower()
                ) == mod.lower():
                    url = messageSplit[0]
                    response = requests.get(url)
                    if response.status_code != 200:
                        return

                    modSplit = response.text.splitlines()
                    verLine = [
                        line for line in modSplit if re.search(r"__version__.*\=.*\(.*\)", line)
                    ]
                    currentVersion = re.sub(r"__version__.*\=", "", verLine[0]).strip()
                    currentVersion = ast.literal_eval(currentVersion)

                    versionList = self.db.get(__name__, "json")
                    versionList[mod] = currentVersion
                    self.db.set(__name__, "json", versionList)

        if (
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "loadmod"
        ) or (
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "loadmod"
            )
        ):
            reply = await message.get_reply_message()
            if reply and not reply.media:
                return

            if reply and not reply.media.document:
                return

            if reply and not reply.media.document.attributes[0].file_name.split('.')[0] == mod:
                return

            if not

            if messageSplit[0] == prefix:
                messageSplit.pop(1)

            messageSplit.pop(0)

            for mod in modList:
                if reply:
                    
                if (
                    messageSplit[0]
                )
