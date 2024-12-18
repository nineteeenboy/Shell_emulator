import zipfile
import os

class VirtualFileSystem:
    """
    Виртуальная файловая система на основе ZIP-архива.
    """
    def __init__(self, zip_path):
        self.zip = zipfile.ZipFile(zip_path, 'r')  # Открываем ZIP-архив
        self.current_path = '/'  # Начинаем с корневого каталога

    def list_directory(self):
        """
        Возвращает список файлов и папок в текущем каталоге.
        """
        prefix = self.current_path.lstrip('/')
        items = set()

        for name in self.zip.namelist():
            if prefix == '':
                # Мы в корне, значит берём элементы верхнего уровня
                if '/' in name:
                    top_element = name.split('/')[0]
                    items.add(top_element)
                else:
                    # Файл в корне без слэшей
                    items.add(name)
            else:
                # В подкаталоге
                if name.startswith(prefix) and name != prefix:
                    relative = name[len(prefix):].lstrip('/')
                    if '/' in relative:
                        # Это подкаталог или файл внутри подкаталога
                        items.add(relative.split('/')[0])
                    else:
                        # Это файл в текущей директории
                        items.add(relative)
        return sorted(items)

    def change_directory(self, path):
        """
        Переход в указанный каталог.
        """
        if path == "..":  # Переход вверх по директориям
            if self.current_path != '/':
                # Удаляем последний сегмент
                parent = os.path.dirname(self.current_path.rstrip('/'))
                if parent == '':
                    self.current_path = '/'
                else:
                    self.current_path = parent + '/'
        else:
            # Формируем новый путь
            new_path = os.path.normpath(os.path.join(self.current_path, path)).replace('\\', '/')
            if not new_path.endswith('/'):
                new_path += '/'

            # Проверяем, что такой каталог существует в zip
            possible_dirs = set()
            for name in self.zip.namelist():
                if name.endswith('/'):
                    possible_dirs.add('/' + name)

            if new_path in possible_dirs:
                self.current_path = new_path
            else:
                raise FileNotFoundError(f"Directory '{path}' does not exist.")

    def move(self, source, destination):
        """
        Симуляция перемещения файла в директорию.
        """
        source_path = os.path.normpath(os.path.join(self.current_path.lstrip('/'), source)).replace('\\', '/')
        destination_path = os.path.normpath(os.path.join(self.current_path.lstrip('/'), destination)).replace('\\', '/')

        # Проверка исходного файла
        if source_path not in self.zip.namelist():
            raise FileNotFoundError(
                f"Файл '{source}' не найден в текущем каталоге '{self.current_path}'."
            )

        # Проверка существования директории назначения
        destination_dir = destination_path if destination_path.endswith('/') else destination_path + '/'
        if not any(d.startswith(destination_dir) for d in self.zip.namelist()):
            raise FileNotFoundError(f"Директория '{destination}' не найдена.")

        # Симуляция перемещения

        clear
        new_path = f"{destination_dir}{os.path.basename(source_path)}"
        print(f"Файл '{source}' перемещён в '{new_path}'. (Симуляция)")

    def read_history(self, history):
        """
        Печатает историю команд.
        """
        for i, command in enumerate(history, 1):
            print(f"{i}: {command}")