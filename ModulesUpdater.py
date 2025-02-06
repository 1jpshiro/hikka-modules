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

__version__ = (1, 0, 0)

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

    strings = {
        "name": "ModulesUpdater",
        "cfg": "Specify True or False if you either want or don't to get suggestion to update",
        "text": "\n\n<b>Your module version isn't up-to-date (<code>{}</code> whereas latest one is <code>{}</code>)\nImperatively recommend you to get updated\nVia: <code>{}</code></b>",
        "log_error": "The module ModulesUpdater just threw an error with status code {} while processing the request to access a file on GitHub\nHere is what it recieved:\n\n{}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Operation",
                True,
                lambda: self.strings["cfg"],
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self):
        path = self.db.get(__name__, "json")
        if not path:
            self.db.set(__name__, "json", {})

    def init(self, modList, loadedMods, versionList):
        modList = modList
        loadedMods = loadedMods
        versionList = versionList

        if loadedMods:
            any_exist = [
                i for i in modList
                for j in loadedMods
                if i == re.sub(r"_"+f"{self.tg_id}"+r"\.py", "", j)
            ]

        if any_exist:
            for item in any_exist:
                if not versionList[item]:
                    with open(f"{abs_path}/{item}.py", "r") as file:
                        file = file.read()
                        fileSplit = file.splitlines()

                    authorLine = [
                        line for line in fileSplit if re.search(r"\#\smeta\sdeveloper\:\s\@shiro\_hikka", line)
                    ][0]
                    if not authorLine:
                        return

                    verLine = [
                        line for line in fileSplit if re.search(r"__version__.*=.*\(.*\)", line)
                    ][0]
                    if not verLine:
                        return

                    currentVersion = re.sub(r"__version__.*\=", "", verLine).strip()
                    versionList[item] = ast.literal_eval(currentVersion)
            self.db.set(__name__, "json", versionList)


    async def watcher(self, message: Message):
        messageSplit = message.text.split()
        modSplit = []
        modName = ""
        prefix = self.get_prefix()
        versionList = self.db.get(__name__, "json")
        aliases = self.db.get("CoreMod", "aliases")

        aliases["help"] = "help"
        aliases["lm"] = "loadmod"
        aliases["dlm"] = "dlmod"

        url = "https://raw.githubusercontent.com/1jpshiro/hikka-modules/main/full.txt"
        full_txt = requests.get(url)
        if full_txt.status_code != 200:
            try:
                logger.error(self.strings["log_error"].format(
                    full_txt.status_code,
                    full_txt.json()
                ))
            except ValueError:
                logger.error(self.strings["log_error"].format(
                    full_txt.status_code,
                    full_txt.text
                ))

        modList = full_txt.text.splitlines()
        path = Path("~/Hikka/loaded_modules")
        abs_path = path.expanduser()
        loadedMods = [
            str(i) for i in abs_path.iterdir() if i.is_file()
        ]

        self.init(modList, loadedMods, versionList)

        if not self.config["Operation"]:
            return

        if len(messageSplit) < 2 or not messageSplit[0].startswith(prefix):
            return

        if any(
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "help"
        ) or any(
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "help"
            )
        ) and len(messageSplit) > 2:
            if messageSplit[0] == prefix:
                messageSplit.pop(1)

            messageSplit.pop(0)

            modName = [
                mod for mod in modList
                if messageSplit[0].lower() == mod.lower()
            ][0]
            if modName:
                modLink = f"https://raw.githubusercontent.com/1jpshiro/hikka-modules/main/{modName}.py"

            if not modName in loadedMods:
                return

            response = requests.get(modLink)
            if response.status_code != 200:
                try:
                    logger.error(self.strings["log_error"].format(
                        full_txt.status_code,
                        full_txt.json()
                    ))
                except ValueError:
                    logger.error(self.strings["log_error"].format(
                        full_txt.status_code,
                        full_txt.text
                    ))

            modSplit = response.text.splitlines()

            verLine = [
                line for line in modSplit if re.search(r"__version__.*\=.*\(.*\)", line)
            ][0]

            _version = re.sub(r"__version__.*\=", "", verLine).strip()
            version = ast.literal_eval(_version)

            currentVersion = versionList[modName]

            if not ((
                version[0] > currentVersion[0]
            ) or (
                version[1] > currentVersion[1]
                and version[0] == currentVersion[0]
            ) or (
                version[2] > currentVersion[2]
                and version[1] == currentVersion[1]
                and version[0] == currentVersion[0]
            )):
                return

            await message.edit(message.text+self.strings["text"].format(
                currentVersion,
                version,
                f".dlm https://raw.githubusercontent.com/1jpshiro/hikka-modules/main/{modName}.py"
            ))

        if any(
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "dlmod"
        ) or any(
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "dlmod"
            )
        ) and len(messageSplit) > 2:
            if messageSplit[0] == prefix:
                messageSplit.pop(1)

            messageSplit.pop(0)

            for mod in modList:
                if (
                    messageSplit[0].split('/')[-1].split('.')[0]
                ) == mod.lower():
                    url = messageSplit[0]
                    response = requests.get(url)
                    if response.status_code != 200:
                        try:
                            logger.error(self.strings["log_error"].format(
                                full_txt.status_code,
                                full_txt.json()
                            ))
                        except ValueError:
                            logger.error(self.strings["log_error"].format(
                                full_txt.status_code,
                                full_txt.text
                            ))

                    modSplit = response.text.splitlines()
                    modName = mod

        if any(
            messageSplit[0].replace(prefix, "") == j 
            for j, i in aliases.items() if i == "loadmod"
        ) or any(
            messageSplit[0] == prefix and any(
                messageSplit[1] == j
                for j, i in aliases.items() if i == "loadmod"
            )
        ) or len(messageSplit) > 2:
            reply = await message.get_reply_message()

            if not (
                hasattr(reply, "media")
                and hasattr(reply.media, "document")
                and reply.media.document.mime_type.split('/')[0] == "text"
            ):
                if not (
                    hasattr(message, "media")
                    and hasattr(message.media, "document")
                    and message.media.document.mime_type.split('/')[0] == "text"
                ):
                    return

                else:
                    with open((await message.download_media()), "r") as file:
                        file = file.read()

            else:
                with open((await reply.download_media()), "r") as file:
                    file = file.read()

            modSplit = file.splitlines()

            authorLine = [
                line for line in modSplit if re.search(r"\#\smeta\sdeveloper\:\s\@shiro\_hikka", line)
            ][0]
            if not authorLine:
                return

            modName = [
                mod for mod in modList
                for line in modSplit
                if re.search(r"class\s"+f"{mod}"+r"\(loader\.Module\)\:", line)
            ][0]

        if not modSplit or not modName:
            return

        verLine = [
            line for line in modSplit if re.search(r"__version__.*\=.*\(.*\)", line)
        ][0]
        if not verLine:
            return

        _currentVersion = re.sub(r"__version__.*\=", "", verLine).strip()
        currentVersion = ast.literal_eval(_currentVersion)

        versionList[modName] = currentVersion
        self.db.set(__name__, "json", versionList)