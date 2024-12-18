# Разработка эмулятора для языка оболочки ОС

## Общее описание
Данный проект реализует эмуляцию командной оболочки с поддержкой базовых команд и виртуальной файловой системы, основанной на zip-архиве. Эмулятор предназначен для работы в режиме командной строки (CLI) и максимально приближен к сеансу работы с shell в UNIX-подобных ОС.

Основные возможности включают:
- Просмотр содержимого директории (`ls`)
- Переход между директориями (`cd`)
- Перемещение файлов (`mv`)
- Просмотр истории команд (`history`)
- Завершение работы (`exit`)

Также поддерживается выполнение стартового скрипта, содержащего список команд, и автоматическое тестирование функционала.

---

## Описание всех функций и настроек

### **Команды эмулятора**:
1. **`ls`**
   - Описание: Показывает список файлов и папок в текущей директории.
   - Пример:
     ```shell
     Выполнение команды: ls
     file1.txt
     file3.txt
     file4.txt
     folder1
     folder2
     folder3
     ```

2. **`cd <путь>`**
   - Описание: Переходит в указанную директорию.
   - Параметры:
     - `..` — переход в родительский каталог.
     - `<folder_name>` — название папки для перехода.
   - Пример:
     ```shell
     Выполнение команды: cd folder1
     ```

3. **`mv <файл> <путь>`**
   - Описание: Перемещает файл в указанную директорию.
   - Параметры:
     - `<файл>` — имя файла для перемещения.
     - `<путь>` — директория, куда переместить файл.
   - Пример:
     ```shell
     Выполнение команды: mv file3.txt folder1/
     Файл 'file3.txt' перемещён в 'folder1/file3.txt'. (Симуляция)
     ```

4. **`history`**
   - Описание: Показывает историю выполненных команд.
   - Пример:
     ```shell
     Выполнение команды: history
     1: ls
     2: cd folder1
     3: cd ..
     4: mv file3.txt folder1/
     ```

5. **`exit`**
   - Описание: Завершает работу эмулятора.

---

## Реализация классов и их функций

### **1. Файл virtual_fs.py (Класс VirtualFileSystem)**
Класс реализует работу с виртуальной файловой системой, основанной на ZIP-архиве. 

#### **Функции:**
1.1 **`__init__(self, zip_path)`** инициализирует виртуальную файловую систему.

````
   def __init__(self, zip_path):
        self.zip = zipfile.ZipFile(zip_path, 'r')  # Открываем ZIP-архив
        self.current_path = '/'  # Начинаем с корневого каталога

````
1.2 **`list_directory(self)`** возвращает список файлов и папок в текущем каталоге.

````
    def list_directory(self):
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

````
1.3 **`change_directory(self, path)`** переходит в указанный каталог.
````
    def change_directory(self, path):
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

````
1.4 **`move(self, source, destination)`** перемещает файл из текущего каталога в указанную директорию (симуляция).
````
    def move(self, source, destination):
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
        new_path = f"{destination_dir}{os.path.basename(source_path)}"
        print(f"Файл '{source}' перемещён в '{new_path}'. (Симуляция)")
````
1.5 **`read_history(self, history)`** показывает историю команд.
````
    def read_history(self, history):
        for i, command in enumerate(history, 1):
            print(f"{i}: {command}")
````
### **2. Файл `cli_handler.py` (Класс ShellCLI)**
Класс отвечает за обработку команд и взаимодействие с виртуальной файловой системой.
#### **Функции:**
2.1 **`__init__(self, username, vfs_path)`** инициализирует оболочку с именем пользователя и виртуальной файловой системой.
````
    def __init__(self, username, vfs_path):
        self.username = username
        self.vfs = VirtualFileSystem(vfs_path)
        self.history = []
````
2.2 **`run_command(self, command)`** выполняет введенную команду.
````
    def run_command(self, command):
        command = command.strip()
        if not command:
            return

        self.history.append(command)
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "ls":
                items = self.vfs.list_directory()
                for item in items:
                    print(item)
            elif cmd == "cd":
                target = args[0] if args else "/"
                self.vfs.change_directory(target)
            elif cmd == "mv":
                if len(args) != 2:
                    print("Использование: mv <источник> <папка_назначения>")
                else:
                    self.vfs.move(args[0], args[1])
            elif cmd == "history":
                self.vfs.read_history(self.history)
            elif cmd == "exit":
                print("Выход из оболочки.")
                exit(0)
            else:
                print(f"Неизвестная команда: {cmd}")
        except Exception as e:
            print(f"Ошибка: {e}")
````
2.3 **`do_ls(self, arg)`** вспомогательная функция для тестов. Выполняет `ls`.
````
    def do_ls(self, arg):
        self.run_command("ls")
````
2.4 **`do_cd(self, arg)`** вспомогательная функция для тестов. Выполняет `cd`.
````
    def do_cd(self, arg):
        arg = arg.strip()
        if not arg:
            arg = "/"
        self.run_command(f"cd {arg}")
````
### **3. Файл `shell_emulator.py` (Главный файл программы)**
Содержит точку входа и логику запуска программы.
#### **Функции:**
3.1 **`main()`**
   - Обрабатывает аргументы командной строки:
     - `-u`: Имя пользователя.
     - `-v`: Путь к ZIP-архиву виртуальной ФС.
     - `-s`: Путь к стартовому скрипту (необязательный).
   - Запускает оболочку и выполняет команды в интерактивном режиме.
````
def main():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки на основе виртуальной ФС.")
    parser.add_argument("-u", "--username", required=True, help="Имя пользователя")
    parser.add_argument("-v", "--vfs", required=True, help="Путь к ZIP-архиву виртуальной ФС")
    parser.add_argument("-s", "--script", help="Путь к стартовому скрипту")

    args = parser.parse_args()
    shell = ShellCLI(args.username, args.vfs)

    if args.script:
        with open(args.script, 'r', encoding='utf-8') as script:
            for line in script:
                line = line.strip()
                if not line:
                    continue
                print(f"Выполнение команды: {line}")
                shell.run_command(line)

    while True:
        command = input(f"{args.username}@vfs:{shell.vfs.current_path}$ ")
        shell.run_command(command)


if __name__ == "__main__":
    main()
````
### **4. Файл `test_vfs.py` (Тестирование VirtualFileSystem)**
#### **Тесты:**
4.1 **`test_list_directory(self)`** проверяет корректность вывода команды `ls`.
````
    def test_list_directory(self):
        files = self.vfs.list_directory()
        self.assertIsInstance(files, list)
````
4.2 **`test_change_directory_success(self)`** проверяет успешный переход в существующую директорию.
````
    def test_change_directory_success(self):
        # Предполагается, что в test_vfs.zip есть папка folder1/
        # Иначе нужно изменить название папки, которая гарантированно есть в тестовом zip
        self.vfs.change_directory("folder1")
        self.assertEqual(self.vfs.current_path, "/folder1/")
````
4.3 **`test_change_directory_fail(self)`** проверяет обработку ошибки при переходе в несуществующую директорию.
````
    def test_change_directory_fail(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.change_directory("nonexistent")
````
### **5. Файл `test_cli.py` (Тестирование ShellCLI)**
#### **Тесты:**
5.1 **`test_ls_command(self)`** проверяет выполнение команды `ls`.
````
    def test_ls_command(self):
        # Проверяем, что команда ls не вызывает ошибок
        self.shell.do_ls("")
        # Можно добавить проверку вывода через mock stdout при необходимости
````
5.2 **`test_cd_command(self)`** проверяет выполнение команды `cd` и корректное обновление пути.
````
    def test_cd_command(self):
        # Проверяем переход в поддиректорию
        # Предполагается, что "folder1" есть в test_vfs.zip
        self.shell.do_cd("folder1")
        self.assertEqual(self.shell.vfs.current_path, "/folder1/")
````


---
## Описание команд для сборки проекта

### **Запуск эмулятора:**
Для запуска эмулятора используйте следующую команду из командной строки:
```bash
python shell_emulator.py -u <имя_пользователя> -v <путь_к_ZIP_архиву> -s <путь_к_стартовому_скрипту>
```
Пример:
```bash
python shell_emulator.py -u user1 -v test_vfs.zip -s startup_script.sh
```
![Ручной ввод](https://github.com/user-attachments/assets/3dcfa989-7a03-4d4e-a6a7-77e68022db77)


### **Запуск тестов:**
```bash
python -m unittest discover -s tests
```
### **Вывод тестов:**
```bash
.file1.txt
file3.txt
file4.txt
folder1
folder2
folder3
....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```
