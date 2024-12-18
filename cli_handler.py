from virtual_fs import VirtualFileSystem

class ShellCLI:
    """
    Обработчик командной строки для виртуальной файловой системы.
    """
    def __init__(self, username, vfs_path):
        self.username = username
        self.vfs = VirtualFileSystem(vfs_path)
        self.history = []

    def run_command(self, command):
        """
        Выполняет введённую команду.
        """
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

    # Для тестов cli, которые вызывают do_ls и do_cd (по аналогии с cmd модулем)
    def do_ls(self, arg):
        self.run_command("ls")

    def do_cd(self, arg):
        arg = arg.strip()
        if not arg:
            arg = "/"
        self.run_command(f"cd {arg}")
