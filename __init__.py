#Author TheStair

#Imports
from binaryninja import *
import sys
from pathlib import Path
import os
import capa.rules
import capa.main
import capa.engine
import capa.features
import capa.loader
import capa.render.json
import capa.render.result_document as rd

# def do_nothing(bv):
#	show_message_box("Do Nothing", "Congratulations! You have successfully done nothing.\n\n" +
#					 "Pat yourself on the back.", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)

# PluginCommand.register("Useless Plugin", "Basically does nothing", do_nothing)

# Prompt for user input and return the filepath
input_file_path_str = ""
def get_input_file():
    global input_file_path_str
    input_file_path_str = input("Please Enter the File to be analyzed: ").strip().lower()
    if input_file_path_str != "":
        file_path = Path(input_file_path_str)
    else:
        print("Please Enter a Filepath")
        sys.exit()
    return file_path

# Writes string of function names and outputs it to a file
def list_file_function_names():

    functions = bv.functions
    str_of_funcs = ""
    for func in functions:
        str_of_funcs += f"Function {func.name} starts at 0x{func.start:x}\n"
    
    output_file_path = os.path.join(output_folder, "list_of_functions.txt")
    with open(output_file_path, "w") as out_file:
        out_file.write(str_of_funcs)
    print("List of Functions located in plugin_output/")


# Capa seems to have very little public documentation.
# I used oxide to try and figure out how to get the information I want
# https://github.com/Program-Understanding/oxide/blob/main/src/oxide/modules/extractors/capa_results/module_interface.py
def capa_analyze(file_path):
    rules_path = Path("/home/thestair/Documents/Program-Analysis/CAPA-Match-Binja/capa-rules-9.1.0")
    #Sets capa's path to the rules
    rules = capa.rules.get_rules([rules_path])

    #Sets the extractor CAPA will use
    extractor = capa.loader.get_extractor(file_path, "auto", "auto", capa.main.BACKEND_VIV, [], False, disable_progress=True,)
    
    #Runs the actual Analysis
    capabilities = counts = capa.main.find_capabilities(
            rules, extractor, disable_progress=True
        )
    
    
    # Fetches additional data
    meta = capa.loader.collect_metadata(
            [], file_path, "auto", "auto", [rules_path], extractor, counts)
    
    doc = rd.ResultDocument.from_capa(meta, rules, capabilities.matches)

    match_str = ""
    for rule_name, matches in capabilities.matches.items():
        match_str += f"Rule: {rule_name}\n"
        for match in matches:
            addr = getattr(match, "address", None)
            match_str += f"  Matched at address: {hex(addr) if addr is not None else 'Unknown'}\n"
    
    # for rule_name, match_list in capabilities.matches.items():
    #     print(f"Rule: {rule_name}")
    #     for i, match in enumerate(match_list):
    #         print(f"  Match #{i} (type: {type(match)}):")
    #         # If match is a list itself, iterate over its elements
    #         if isinstance(match, list):
    #             for j, submatch in enumerate(match):
    #                 print(f"    Submatch #{j} (type: {type(submatch)}): {submatch}")
    #         else:
    #             print(f"    {match}")
    #     # Just inspect one rule for now
    #     break

    output_file_path = os.path.join(output_folder, "capa_capabilities.csv")
    with open(output_file_path, "w") as out_file:
        out_file.write(str(capabilities))

    output_file_path = os.path.join(output_folder, "capa_metadata.csv")
    with open(output_file_path, "w") as out_file:
        out_file.write(str(meta))
    
    output_file_path = os.path.join(output_folder, "capa_results.csv")
    with open(output_file_path, "w") as out_file:
        out_file.write(str(doc))
    
    output_file_path = os.path.join(output_folder, "formatted_capa_results.txt")
    with open(output_file_path, "w") as out_file:
        out_file.write(match_str)

    print("List capa capabilities located in plugin_output/")
    return 0


#Script Start
#Loads user-specified file
input_file = get_input_file()
with load(input_file) as bv:
    print("Loaded file into Binary Ninja")


# Make output folder
output_folder = "plugin_output"
os.makedirs(output_folder, exist_ok=True)

list_file_function_names()
capa_analyze(input_file)