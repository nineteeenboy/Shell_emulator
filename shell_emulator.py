import argparse
from cli_handler import ShellCLI

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
