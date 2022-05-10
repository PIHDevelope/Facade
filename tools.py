import abc
from dataclasses import dataclass
from typing import Dict, List


class NotImplemented(BaseException):
    pass


class UserInterruption(BaseException):
    pass


class CommandNameIsExistsAlready(BaseException):
    pass


class CommandFullFileNameIsExistAlready(Exception):
    pass


class CommandNameIsNotExists(Exception):
    pass


@dataclass
class Command:
    group: str
    command_name: str
    file: str
    description: str
    section: str


class CommandList():

    def __init__(self):
        self.list: List[Command] = []
        self.name_dict: Dict[str, Command] = {}
        self.index_dict: Dict[int, str] = {}
        self.index = 0

    def length(self) -> int:
        return len(self.list)

    def get_by_index(self, index: int) -> Command:
        return self.name_dict[self.index_dict[index]]

    def get_by_name(self, name: str) -> Command:
        return self.name_dict[name]

    def register_command(self, command: Command) -> None:
        def get_command_file_name(command: Command) -> str:
            return command.group + command.file + command.section
        if command.command_name in map(lambda item: item.command_name, self.list):
            raise CommandNameIsExistsAlready()
        if get_command_file_name(command) in map(lambda item: get_command_file_name(item), self.list):
            raise CommandFullFileNameIsExistAlready(
                f"{command.command_name}: {get_command_file_name(command)}")
        self.list.append(command)
        self.name_dict[command.command_name] = command
        self.index_dict[self.length() - 1] = command.command_name

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index > self.length():
            self.index = 0
            raise StopIteration
        return self.index, self.get_by_index(self.index - 1)


def create_command(command_name: str, description: str, group: str, file: str, section: str = "") -> Command:
    return Command(group, command_name, file, description, section)


class ICommandListStorage(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "get_command_list") and
                callable(subclass.get_command_list) or
                NotImplemented)

    @abc.abstractmethod
    def get_command_list(self) -> CommandList:
        raise NotImplemented


LOCAL_COMMAND_LIST: dict = {
    #name : [prefix, command, description]
    "Telegram_message":         ["Telegram", "message.lnk", "Telegram message"],
    #
    "AD_findByLogin":           ["ActiveDirectory", "findBy.py", "Find by login", "samAccountName"],
    "AD_findByName":            ["ActiveDirectory", "findBy.py", "Find by name",  "name"],
    "AD_findByLogin2":          ["ActiveDirectory", "findByLogin.ps1", "Find by login (PowerShell version)"],
    "AD_findBySurname2":        ["ActiveDirectory", "findBySurname.ps1", "Find by surname (PowerShell version)"],
    "AD_checker":               ["ActiveDirectory", "checker.ps1", "Check by rules (PowerShell version)"],
    "AD_checkOrAddDeadUser":    ["ActiveDirectory", "checkOrAddDeadUser.ps1", "Find by login (PowerShell version)"],
    #
    "Polibase_ping":            ["Polibase", "ping.lnk", "Ping Polibase [message]"],
    "Polibase_dbDump":          ["Polibase", "dbDump.lnk", "Create Polibase database Dump"],
    #
    "Orion_findByTabNumber":    ["Orion", "findByTabNumber.lnk", "Find person by tab number"],
    "Orion_findByName":         ["Orion", "findByName.lnk", "Find person by name"],
    "Orion_checker":            ["Orion", "checker.lnk", "Check by rules"]
}


class LocalCommandListStorage(ICommandListStorage):

    def __init__(self, command_list_dict: dict = LOCAL_COMMAND_LIST):
        self.command_list = command_list_dict
        self.list: CommandList = CommandList()
        for command_name in self.command_list:
            command = self.convert_to_command_by_name(command_name)
            self.list.register_command(command)

    def convert_to_command_by_name(self, name: str) -> Command:
        if name not in self.command_list:
            raise CommandNameIsNotExists
        commnad_object = self.command_list[name]
        return Command(commnad_object[0], name, commnad_object[1],
                       commnad_object[2], "" if len(commnad_object) < 4 else commnad_object[3])

    def get_command_list(self) -> CommandList:
        return self.list


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
