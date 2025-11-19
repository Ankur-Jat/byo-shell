import os
from pathlib import Path
import subprocess
import sys


def _search_executable(arg):
    path = os.getenv("PATH", "")
    for sub_path in path.split(os.pathsep):
        if os.path.exists(sub_path):
            for root, _, files in os.walk(sub_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file == arg and  os.access(file_path, os.X_OK):
                        return file_path
    return None


def run_executable(arg):
    command = arg.split(" ")[0]
    executable_path = _search_executable(command)
    if executable_path:
        subprocess.run(arg.split(" "))
        return True
    return False


def command_type(arg):
    if arg in ["echo", "exit", "type", "pwd"]:
        sys.stdout.write(f"{arg} is a shell builtin\n")
        return
    file_path = _search_executable(arg)
    if file_path:
        sys.stdout.write(f"{arg} is {file_path}\n")
        return
    sys.stdout.write(f"{arg}: not found\n")


def command_pwd():
    print(os.getcwd())


def command_echo(arg):
    sys.stdout.write(arg + "\n")


def main():
    while True:
        sys.stdout.write("$ ")
        command = input("")
        if command == "exit 0":
            break
        if command.startswith("echo "):
            command_echo(command[5:])
        elif command.startswith("type "):
            command_type(command[5:])
        elif command == "pwd":
            command_pwd()
        elif not run_executable(command):
            sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
