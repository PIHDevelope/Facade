# Facade for Pacific International Hospital (init version)
import os
import subprocess
import sys
from typing import List

import win32com.client
from prettytable import PrettyTable

from tools import Bcolors, Command, CommandList, NotImplemented, create_command, LocalCommandListStorage

command_list: CommandList = LocalCommandListStorage().get_command_list()
#
FACADE_PATH = "//fmv/facade/"
COMMAND_SUFFIX = "Commands"
LINK_EXT = "lnk"
#
PYTHON_EXECUTOR = "python"
POWERSHELL_EXECUTOR = "powershell"
DEFAULT_EXECUTOR = PYTHON_EXECUTOR

executor_dict = {
    "": DEFAULT_EXECUTOR,
    "py": PYTHON_EXECUTOR,
    "ps1": POWERSHELL_EXECUTOR
}


def get_file_extension(file: str) -> str:
    return "" if file.find(".") == -1 else file.split(".")[-1]


def convert_command_to_command_file_path(command: Command, shell) -> str:
    return shell.CreateShortCut(command.file).Targetpath if get_file_extension(command.file) == "lnk" else command.file


def get_executor_path(path: str) -> str:
    return executor_dict[get_file_extension(path)]


def convert_command_file_path_for_executor(path: str, executor: str) -> str:
    if executor == POWERSHELL_EXECUTOR:
        path = f".\\{path}"
    return path


def get_command_group_path(command: Command) -> str:
    return f"{FACADE_PATH}{command.group}{COMMAND_SUFFIX}"


def set_cwd(path: str) -> None:
    os.chdir(path)


def run_command_line(command: List[str]) -> None:
    result = subprocess.run(command, capture_output=False, text=True)
    if result.returncode != 0:
        # if result.stderr.find("cl.NotImplemented") != -1:
        raise NotImplemented()


def get_command_line(executor: str, command_file_path: str, command_section: str, params: List[str]) -> List[str]:
    command_output = []
    command_output.append(executor)
    command_output.append(command_file_path)
    if command_section != "":
        command_output.append(command_section)
    if params is not None:
        for param in params:
            command_output.append(param)
    return command_output


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def main(argv):
    #
    command: Command = None
    #
    params: List[str] = None
    #
    table = PrettyTable(["Index", "Name", "Description"])
    table.align["Name"] = "l"
    table.align["Description"] = "l"
    try:
        if len(argv) == 1:
            print(f"{Bcolors.HEADER}Command list:{Bcolors.ENDC}")
            for index, command_local in command_list:
                table.add_row(
                    [str(index),  f"{Bcolors.OKBLUE}{command_local.command_name}{Bcolors.ENDC}", command_local.description])
            print(table)
            command_list_len = command_list.length()
            #
            try:
                command_index = input(
                    f"Enter index command (from 1 to {command_list_len}) : ")
                command_index = int(command_index) - 1
                command = command_list.get_by_index(command_index)
            except (KeyError, ValueError):
                print(
                    f"{Bcolors.FAIL}Enter number of command [from 1 to {command_list_len}]!{Bcolors.ENDC}")
        else:
            try:
                command = command_list.get_by_name(argv[1])
                params = argv[2:]
            except KeyError:
                print(f"{Bcolors.FAIL}Commnad is not exists!{Bcolors.ENDC}")
        if command is not None:
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                #
                set_cwd(get_command_group_path(command))
                #
                command_file_path = convert_command_to_command_file_path(
                    command, shell)
                #
                executor = get_executor_path(command_file_path)
                #
                command_file_path = convert_command_file_path_for_executor(
                    command_file_path, executor)
                #
                command_line = get_command_line(
                    executor, command_file_path, command.section, params)
                #
                try:
                    run_command_line(command_line)
                except KeyboardInterrupt:
                    print(f"{Bcolors.FAIL}Interrupt by user...{Bcolors.ENDC}")
                except NotImplemented:
                    print(f"{Bcolors.FAIL}Not implemented...{Bcolors.ENDC}")
            except KeyError:
                raise ValueError(f"Undefined command: {command}")
    except KeyboardInterrupt:
        print(f"{Bcolors.FAIL}Main: Interrupt by user...{Bcolors.ENDC}")


if __name__ == "__main__":
    argv = sys.argv
    run_once = len(argv) > 1
    while True:
        main(argv)
        if run_once:
            break
