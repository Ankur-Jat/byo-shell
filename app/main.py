import os
import shlex
from pathlib import Path
import subprocess
import sys


BUILT_IN = {
    "echo": lambda x: print(" ".join(x)),
    "type": lambda x: command_type(x[0]),
    "pwd": lambda _: print(os.getcwd()),
    "cd": lambda x: command_cd(x),
    "exit": lambda _: exit(0)
}


def handle_single_quote_args(args: list[str]) -> list[str]:
    return args


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


def run_executable(command, args):
    executable_path = _search_executable(command)
    if executable_path:
        subprocess.run([command] + args)
        return True
    return False


def command_type(arg):
    if arg in BUILT_IN:
        sys.stdout.write(f"{arg} is a shell builtin\n")
        return
    file_path = _search_executable(arg)
    if file_path:
        sys.stdout.write(f"{arg} is {file_path}\n")
        return
    sys.stdout.write(f"{arg}: not found\n")


def command_cd(arg):
    if len(arg) != 1:
        raise Exception("cd commange needs one argument. Argument is missing")
    if arg[0].strip() == "~":
        os.chdir(os.getenv("HOME"))
    elif os.path.isdir(arg[0]):
        os.chdir(arg[0])
    else:
        print(f"cd: {arg[0]}: No such file or directory")


def main():
    while True:
        sys.stdout.write("$ ")
        cmd_input = input("")
        if not cmd_input.strip():
            print("\n")
            continue
        if ">" in cmd_input or "1>" in cmd_input:
            os.system(cmd_input)
            continue
        parts = shlex.split(cmd_input)
        command, args = parts[0], parts[1:]
        if command in BUILT_IN:
            BUILT_IN[command](args)
        elif not run_executable(command, args):
            sys.stdout.write(f"{cmd_input}: command not found\n")


if __name__ == "__main__":
    main()
