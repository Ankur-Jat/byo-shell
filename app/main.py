import os
from pathlib import Path
import sys


def command_type(arg):
    if arg in ["echo", "exit", "type"]:
        sys.stdout.write(f"{arg} is a shell builtin\n")
        return
    path = os.getenv("PATH", "")
    for sub_path in path.split(os.pathsep):
        if os.path.exists(sub_path):
            for root, _, files in os.walk(sub_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file == arg and  os.access(file_path, os.X_OK):
                        sys.stdout.write(f"{arg} is {file_path}\n")
                        return
    sys.stdout.write(f"{arg}: not found\n")


def main():
    while True:
        sys.stdout.write("$ ")
        command = input("")
        if command == "exit 0":
            break
        if command.startswith("echo "):
            sys.stdout.write(command[5:] + "\n")
            continue
        if command.startswith("type "):
            type_command = command[5:]
            command_type(type_command)
            continue
        sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
