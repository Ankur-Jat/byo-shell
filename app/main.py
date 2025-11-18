import sys


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
            if type_command in ["echo", "exit", "type"]:
                sys.stdout.write(f"{type_command} is a shell builtin\n")
            else:
                sys.stdout.write(f"{type_command}: not found\n")
            continue
        sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
