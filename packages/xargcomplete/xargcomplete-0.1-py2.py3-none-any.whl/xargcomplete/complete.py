# coding:utf-8

from base64 import b16decode
from base64 import b16encode
from configparser import ConfigParser
import os
from typing import Iterable
from typing import Optional
from typing import Set

from pip._internal.commands.show import _PackageInfo
from pip._internal.commands.show import search_packages_info
from xkits_command.attribute import __project__ as command_project

from xargcomplete.attribute import __project__


class Bash:
    USER_COMPLETION_CFG = "~/.bash_completion"
    USER_COMPLETION_DIR = "~/.bash_completion.d"
    COMPLETION_PATH = os.path.expanduser(USER_COMPLETION_CFG)
    COMPLETION_HOOK = os.path.expanduser(USER_COMPLETION_DIR)
    COMPLETION_CODE = """
for bcfile in ~/.bash_completion.d/* ; do
  source ${bcfile}
done
"""

    @classmethod
    def enable(cls):
        if not os.path.exists(cls.COMPLETION_HOOK):
            os.makedirs(cls.COMPLETION_HOOK)

        with open(cls.COMPLETION_PATH, "r", encoding="utf-8") as fh:
            if cls.COMPLETION_CODE in fh.read():
                return

        with open(cls.COMPLETION_PATH, "a", encoding="utf-8") as fh:
            fh.write(f"\n{cls.COMPLETION_CODE}\n")

        cls.update(__project__)

    @classmethod
    def update(cls, cmd: str) -> int:
        bash_completion_hook = os.path.expanduser(cls.USER_COMPLETION_DIR)
        name = b16encode(cmd.encode()).decode()
        path = os.path.join(bash_completion_hook, f"{__project__}-{name}")
        return os.system(f"register-python-argcomplete {cmd} > {path}")

    @classmethod
    def remove(cls, cmd: str) -> bool:
        bash_completion_hook = os.path.expanduser(cls.USER_COMPLETION_DIR)
        name = b16encode(cmd.encode()).decode()
        path = os.path.join(bash_completion_hook, f"{__project__}-{name}")
        if os.path.isfile(path):
            os.remove(path)
        return not os.path.exists(path)

    @classmethod
    def list(cls) -> Set[str]:
        cmds: Set[str] = set()
        bash_completion_hook = os.path.expanduser(cls.USER_COMPLETION_DIR)
        if not os.path.exists(bash_completion_hook):
            os.makedirs(bash_completion_hook)
        for item in os.listdir(bash_completion_hook):
            if not os.path.isfile(os.path.join(bash_completion_hook, item)):
                continue
            keys = item.split("-", 1)
            if len(keys) == 2 and keys[0] == __project__:
                cmds.add(b16decode(keys[1]).decode())
        return cmds


class Collections:

    __INSTANCE: Optional["Collections"] = None
    __INITIALIZED: bool = False

    def __init__(self):
        if not self.__INITIALIZED:
            self.__cmds: Set[str] = set()
            for _pkg in tuple({"argcomplete", command_project}):
                for _req in set(self.get_package_info(_pkg).required_by):
                    config = ConfigParser()
                    package_info = self.get_package_info(_req)
                    config.read_string(os.linesep.join(
                        package_info.entry_points))
                    if config.has_section("console_scripts"):
                        for _cmd in config["console_scripts"]:
                            self.__cmds.add(_cmd)

    def __new__(cls):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super(Collections, cls).__new__(cls)
        return cls.__INSTANCE

    @property
    def cmds(self) -> Iterable[str]:
        return iter(self.__cmds)

    @classmethod
    def get_package_info(cls, package_name: str) -> _PackageInfo:
        return list(search_packages_info([package_name]))[0]
