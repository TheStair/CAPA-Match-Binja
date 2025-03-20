#Author TheStair

#Imports
from binaryninja import *
import sys
from pathlib import Path

# def do_nothing(bv):
#	show_message_box("Do Nothing", "Congratulations! You have successfully done nothing.\n\n" +
#					 "Pat yourself on the back.", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)

# PluginCommand.register("Useless Plugin", "Basically does nothing", do_nothing)

# Prompt for user input and return the filepath
def get_input_file():
    input_file_path_str = input("Please Enter the File to be analyzed: ").strip().lower()
    if input_file_path_str != "":
        file_path = Path(input_file_path_str)
    else:
        print("Please Enter a Filepath")
        sys.exit()
    return file_path

# Prints Funtion Names and Addresses (Mostly a Test function)
def print_file_function_names():

    functions = bv.functions
    for func in functions:
        print(f"Function {func.name} starts at 0x{func.start:x}")


#Script Start
#Loads user-specified file
input_file = get_input_file()
with load(input_file) as bv:
    print("Analyzing File")

print_file_function_names()