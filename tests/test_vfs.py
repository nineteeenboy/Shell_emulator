import unittest
import sys
import os

# Добавляем путь к родительской директории
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from virtual_fs import VirtualFileSystem
from cli_handler import ShellCLI


class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem("test_vfs.zip")

    def test_list_directory(self):
        files = self.vfs.list_directory()
        self.assertIsInstance(files, list)

    def test_change_directory_success(self):
        # Предполагается, что в test_vfs.zip есть папка folder1/
        # Иначе нужно изменить название папки, которая гарантированно есть в тестовом zip
        self.vfs.change_directory("folder1")
        self.assertEqual(self.vfs.current_path, "/folder1/")

    def test_change_directory_fail(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.change_directory("nonexistent")
