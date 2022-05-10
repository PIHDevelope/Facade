import unittest
import sys


sys.path.append("\\\\fmv\\facade")
from tools import *

COMMAND_NAME = "command_name"
DESCRIPTION = "description"
GROUP = "group_name"
FILE = "file_name"
SECTION = "section"

class TestLocalStorage(unittest.TestCase):

    def test_for_LocalCommandListStorage_is_implemented_ICommandListStorage(self):
        try:
            storage = LocalCommandListStorage()
        except NotImplemented:
            self.fail("Raised NotImplemented")

    def test_for_fail_convert_to_command_by_name_that_is_not_exists(self):
        storage = LocalCommandListStorage()
        result = False
        try:
            storage.convert_to_command_by_name(COMMAND_NAME)
        except CommandNameIsNotExists:
            result = True
        self.assertEqual(result, True)

    def test_for_convert_to_command_by_name_that_is_exists(self):
        storage = LocalCommandListStorage()
        command = storage.convert_to_command_by_name("AD_findByName")
        self.assertEqual(command.command_name, "AD_findByName")
        self.assertEqual(command.group, "ActiveDirectory")
        self.assertEqual(command.file, "findBy.py")
        self.assertEqual(command.description, "Find by name")
        self.assertEqual(command.section, "name")

    def test_for_convert_to_command_by_name_that_is_exists2(self):
        storage = LocalCommandListStorage()
        command = storage.convert_to_command_by_name("Telegram_message")
        self.assertEqual(command.command_name, "Telegram_message")
        self.assertEqual(command.group, "Telegram")
        self.assertEqual(command.file, "message")
        self.assertEqual(command.description, "Telegram message")
        self.assertEqual(command.section, "")


    def test_get_command_list(self):
        command_list = LocalCommandListStorage().get_command_list()
        self.assertEqual(command_list.length(), len(LOCAL_COMMAND_LIST))

    def test_for_convert_to_command_by_name_that_is_exists(self):
        storage = LocalCommandListStorage()
        self.assertIsInstance(
                storage.convert_to_command_by_name("AD_findByLogin"), Command)


class TestCreateCommand(unittest.TestCase):

    def test_create_command_returns_right_type(self):
        self.assertIsInstance(create_command(
            COMMAND_NAME,   DESCRIPTION,
            GROUP,  FILE,  SECTION), Command)

    def test_create_command_with_out_section_parameter(self):
        self.assertIsInstance(create_command(
            COMMAND_NAME,   DESCRIPTION,
            GROUP,  FILE), Command)

    def test_create_command_with_out_section_parameter(self):
        command = create_command(
            COMMAND_NAME,   DESCRIPTION,
            GROUP,  FILE, SECTION)
        self.assertEqual(command.command_name, COMMAND_NAME)
        self.assertEqual(command.description, DESCRIPTION)
        self.assertEqual(command.group, GROUP)
        self.assertEqual(command.file, FILE)
        self.assertEqual(command.section, SECTION)


class TestCommandList(unittest.TestCase):

    def test_register_command_returns_false_if_command_name_is_not_unique(self):
        commandList = CommandList()
        result = False
        try:
            commandList.register_command(create_command(
                COMMAND_NAME,   DESCRIPTION,
                GROUP,  FILE, SECTION))
            commandList.register_command(
                create_command(
                    COMMAND_NAME,   DESCRIPTION,
                    GROUP,  FILE))
            result = True
        except CommandNameIsExistsAlready:
            pass
        self.assertEqual(result, False)

    def test_register_command_returns_true_if_commands_is_unique(self):
        commandList = CommandList()
        result = True
        commandList.register_command(
            create_command(
                COMMAND_NAME,   DESCRIPTION,
                GROUP,  FILE, SECTION))
        try:
            commandList.register_command(
                create_command(
                    f"{COMMAND_NAME}2",   DESCRIPTION,
                    f"{GROUP}2",  FILE, SECTION))
        except CommandNameIsExistsAlready:
            result = False
        self.assertEqual(result, True)

    def test_register_command_returns_false_if_group_plus_file_is_not_unique(self):
        commandList = CommandList()
        result = True
        commandList.register_command(
            create_command(
                COMMAND_NAME,   DESCRIPTION,
                GROUP,  FILE))
        try:
            commandList.register_command(
                create_command(
                    f"{COMMAND_NAME}2",   DESCRIPTION,
                    GROUP,  FILE))
        except CommandFullFileNameIsExistAlready:
            result = False
        self.assertEqual(result, False)

    def test_register_command_returns_true_if_group_file_section_is_unique(self):
        commandList = CommandList()
        result = True
        try:
            commandList.register_command(
                create_command(
                    COMMAND_NAME,   DESCRIPTION,
                    GROUP,  FILE))
            commandList.register_command(create_command(
                f"{COMMAND_NAME}2",   DESCRIPTION,
                GROUP,  FILE, SECTION))
        except CommandFullFileNameIsExistAlready:
             result = False
        self.assertEqual(result, True)   


    def test_register_command_returns_true_if_group_file_section_is_unique2(self):
        commandList = CommandList()
        result = True
        try:
            commandList.register_command(
                create_command(
                    COMMAND_NAME,   DESCRIPTION,
                    GROUP,  FILE, f"{SECTION}2"))
            commandList.register_command(create_command(
                f"{COMMAND_NAME}2",   DESCRIPTION,
                GROUP,  FILE, SECTION))
        except CommandFullFileNameIsExistAlready:
            result = False
        self.assertEqual(result, True)

    def test_register_command_returns_len_equal_2_if_group_file_section_is_unique(self):
        commandList = CommandList()
        commandList.register_command(create_command(
            COMMAND_NAME,   DESCRIPTION,
            GROUP,  FILE))
        commandList.register_command(create_command(
            f"{COMMAND_NAME}2",   DESCRIPTION,
            GROUP,  FILE, SECTION))
        self.assertEqual(commandList.length(), 2)

    def test_register_command_returns_len_equal_2_if_group_file_section_is_unique2(self):
        commandList = CommandList()
        commandList.register_command(create_command(
            COMMAND_NAME,   DESCRIPTION,
            GROUP,  FILE, f"{SECTION}2"))
        commandList.register_command(create_command(
            f"{COMMAND_NAME}2",   DESCRIPTION,
            GROUP,  FILE, SECTION))
        self.assertEqual(commandList.length(), 2)

    def test_register_command_returns_len_equal_1_if_group_file_section_is_not_unique(self):
        commandList = CommandList()
        try:
            commandList.register_command(create_command(
                COMMAND_NAME,   DESCRIPTION,
                GROUP,  FILE, f"{SECTION}2"))
        except CommandNameIsExistsAlready:
            pass
        try:
            commandList.register_command(create_command(
                COMMAND_NAME,   DESCRIPTION,
                GROUP,  FILE, SECTION))
        except CommandNameIsExistsAlready:
            pass
        self.assertEqual(commandList.length(), 1)


if __name__ == "__main__":
    unittest.main()
