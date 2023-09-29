import sys
import subprocess
import os
from os import listdir
from os.path import isfile, join, getmtime, getsize
import time

# Define the list of allowed inner commands and cmd commands
inner_cmds = {
    "exit": "exit the cmd program",
    "help": "Provides help information for commands",
    "cd": "Displays the name of or changes the current directory",
    "set": "Displays, sets, or removes cmd.exe environment variables."
}
external_cmds = {
    "dir": "List files and directories in the current directory",
    "type": "Display the contents of a text file",
    "time": "Display or set the system time",
    "ls": "Custom directory listing",
}


def custom_ls(mypath):
    try:
        items = listdir(mypath)

        for item in items:
            full_name = join(mypath, item)
            if isfile(full_name):
                print(f"{time.ctime(getmtime(full_name))}\t\t{str(getsize(full_name))}\t{item}")
            else:
                print(f"{time.ctime(getmtime(full_name))}\t<Dir>\t\t{item}")
    except Exception as e:
        print("Error in custom_ls:", str(e))

def set_command(args):
    if len(args) != 2:
        print("Usage: set <variable_name>=<value>")
        return

    # Split the argument into variable name and value
    variable, value = args[1].split("=")

    # Set the environment variable
    os.environ[variable] = value

    print(f"Set {variable}={value}")

def handle_inner_command(command, arguments):
    try:
        if command == "exit":
            sys.exit(0)
        elif command == "help":
            if arguments:
                # Display help for a specific command
                cmd = arguments[0]
                if cmd in external_cmds:
                    print(f"{cmd}: {external_cmds[cmd]}")
                else:
                    print("Command not found.")
            else:
                # Display available inner commands and cmd commands
                print("----------------inner----------------")
                for cmd, description in inner_cmds.items():
                    print(f"{cmd}: {description}")
                print("----------------cmd----------------")
                for cmd, description in external_cmds.items():
                    print(f"{cmd}: {description}")
        elif command == "cd":
            try:
                # Change directory using subprocess
                subprocess.run(["cd"] + arguments, shell=True)
            except Exception as e:
                print("Error in cd:", str(e))
        elif command == "set":
            set_command(arguments)
        else:
            print("Command not recognized. Type 'help' for available commands.")
    
    except Exception as e:
        print("Error in handle_inner_command:", str(e))


def handle_external_command(command, arguments):
    try:
        if command == "ls":
            # Call the custom_ls function with the current directory
            custom_ls(os.getcwd())
        else:
            # Execute cmd commands using subprocess
            subprocess.run([command] + arguments, shell=True)
    except Exception as e:
        print("Error in handle_cmd_command:", str(e))


def main():
    while True:
        # Get the current working directory
        current_directory = os.getcwd()
        # Prompt the user for input with the current directory
        user_input = input(f"GuyRazCMD-{current_directory}> ").strip()

        # Split the user input into command and arguments
        input_parts = user_input.split()
        command = input_parts[0].lower()
        arguments = input_parts[1:]

        if command in inner_cmds:
            handle_inner_command(command, arguments)
        elif command in external_cmds:
            handle_external_command(command, arguments)
        else:
            print("Command not recognized. Type 'help' for available commands.")


if __name__ == "__main__":
    main()