import sys
import subprocess
import os
from os import listdir
from os.path import isfile, join, getmtime, getsize
import time
from datetime import datetime

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


def custom_ls(args):
    if len(args) == 0:
        # Perform ls in the current directory
        files = os.listdir()
        for file in files:
            print(file)
    elif len(args) == 1:
        try:
            # Change directory to the specified directory
            mypath = os.path.join(os.getcwd(), args[0])
            os.chdir(mypath)

            # Perform ls in the specified directory
            files = os.listdir()
            for file in files:
                print(file)
        except FileNotFoundError:
            print("Directory not found.")
    else:
        print("Invalid command. Usage: custom_ls [directory]")

def set_command(args):
    if len(args) == 0:
        # Display all environment variables
        for var in os.environ:
            print(f"{var}={os.environ[var]}")
    elif len(args) != 1:
        print("Usage: set <variable_name>=<value>")
    else:
        # Split the argument into variable name and value
        variable, value = args[0].split("=")
    
        # Set the environment variable
        os.environ[variable] = value
    
        print(f"Set {variable}={value}")

def change_directory(args):

    # print current directory 
    if len(args) == 0:
        print(os.getcwd())
        return
    
    args = args[0]
    if not os.path.isdir(args) and args != "":
        print("The system cannot find the path specified.")
        return
    
    dir = os.getcwd()
    
    if args == '/' or args == '\\':
        dir = os.chdir("/")

    else:
        new_path = args
        # Change the PATH environment variable to the new full path
        os.environ["PATH"] = new_path
        dir = new_path
        
    os.chdir(dir)
    return dir




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
                change_directory(arguments)
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
            custom_ls(arguments)
        elif command == "time":
            print(datetime.now().time())
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