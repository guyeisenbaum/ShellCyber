import sys
import subprocess
import os
from os import listdir
from os.path import isfile, join, getmtime, getsize
import time

# Define the list of allowed inner commands and cmd commands
inner_cmds = {
    "exit": "exit the cmd program ",
    "help": "",
    "cd": "",
    "set": "set enviromental variables" }
cmd_cmds = {
    "dir": "List files and directories in the current directory",
    "type": "Display the contents of a text file",
    "time": "Display or set the system time",
    "ls": "Custom directory listing",
}


def custom_ls(mypath):
    items = listdir(mypath)

    for item in items:
        full_name = join(mypath, item)
        if isfile(full_name):
            print(f"{time.ctime(getmtime(full_name))}\t\t{str(getsize(full_name))}\t{item}")
        else:
            print(f"{time.ctime(getmtime(full_name))}\t<Dir>\t\t{item}")


def handle_inner_command(command, arguments):
    if command == "exit":
        sys.exit(0)
    elif command == "help":
        if arguments:
            # Display help for a specific command
            cmd = arguments[0]
            if cmd in cmd_cmds:
                print(f"{cmd}: {cmd_cmds[cmd]}")
            else:
                print("Command not found.")
        else:
            # Display available inner commands and cmd commands
            print("Available inner commands:", inner_cmds)
            print("Available cmd commands:")
            for cmd, description in cmd_cmds.items():
                print(f"{cmd}: {description}")
    elif command == "cd":
        try:
            # Change directory using subprocess
            subprocess.run(["cd"] + arguments, shell=True)
        except Exception as e:
            print("Error:", str(e))
    elif command == "set":
        print("Setting variables is not implemented in this example.")
    else:
        print("Command not recognized. Type 'help' for available commands.")


def handle_cmd_command(command, arguments):
    if command == "ls":
        # Call the custom_ls function with the current directory
        custom_ls(os.getcwd())
    else:
        try:
            # Execute cmd commands using subprocess
            subprocess.run([command] + arguments, shell=True)
        except Exception as e:
            print("Error:", str(e))


def main():
    while True:
        # Get the current working directory
        current_directory = os.getcwd()
        # Prompt the user for input with the current directory
        user_input = input(f"GuyRazCMD-{current_directory}> ").strip()

        # Split the user input into command and arguments
        input_parts = user_input.split()
        command = input_parts[0]
        arguments = input_parts[1:]

        if command in inner_cmds:
            handle_inner_command(command, arguments)
        elif command in cmd_cmds:
            handle_cmd_command(command, arguments)
        else:
            print("Command not recognized. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
