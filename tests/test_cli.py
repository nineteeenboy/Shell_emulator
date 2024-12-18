import unittest
import sys
import os

# Добавляем путь к родительской директории
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cli_handler import ShellCLI


class TestShellCLI(unittest.TestCase):
    def setUp(self):
        self.shell = ShellCLI("testuser", "test_vfs.zip")

    def test_ls_command(self):
        # Проверяем, что команда ls не вызывает ошибок
        self.shell.do_ls("")
        # Можно добавить проверку вывода через mock stdout при необходимости

    def test_cd_command(self):
        # Проверяем переход в поддиректорию
        # Предполагается, что "folder1" есть в test_vfs.zip
        self.shell.do_cd("folder1")
        self.assertEqual(self.shell.vfs.current_path, "/folder1/")
