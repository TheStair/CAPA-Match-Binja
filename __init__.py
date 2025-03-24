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
import re

# Writes string of function names and outputs it to a file
# def list_file_function_names():

#     functions = bv.functions
#     str_of_funcs = ""
#     for func in functions:
#         str_of_funcs += f"Function {func.name} starts at 0x{func.start:x}\n"
    
#     output_file_path = os.path.join(output_folder, "list_of_functions.txt")
#     with open(output_file_path, "w") as out_file:
#         out_file.write(str_of_funcs)
#     print("List of Functions located in plugin_output/")



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


# Capa seems to have very little public documentation.
# I used oxide to try and figure out how to get the information I want
# https://github.com/Program-Understanding/oxide/blob/main/src/oxide/modules/extractors/capa_results/module_interface.py

# Runs CAPA Analysis and returns a JSON for each function with a match.
# Each JSON contains the function name, address, matched rules, and disassembly
# After looking throught the CAPA repo, I found that capa has a binary ninja backend. So to avoid wrestling
# with different address spaces, I opted to use their binja backend
def capa_analyze(file_path):
    print("Running CAPA Analysis")
    rules_path = Path("/home/thestair/Documents/Spring-2025/Program Analysis/CAPA-Match-Binja/capa-rules-9.1.0/")
    # rules_path = Path("/home/thestair/Documents/Program-Analysis/CAPA-Match-Binja/capa-rules-9.1.0")
    #Sets capa's path to the rules
    rules = capa.rules.get_rules([rules_path])

    #Sets the extractor CAPA will use 
    extractor = capa.loader.get_extractor(file_path, "auto", "auto", capa.main.BACKEND_BINJA, [], False, disable_progress=True,)
    
    #Runs the actual Analysis
    capabilities = counts = capa.main.find_capabilities(
            rules, extractor, disable_progress=True
        )

    
    # Fetches additional data (Not really used)
    # meta = capa.loader.collect_metadata(
    #         [], file_path, "auto", "auto", [rules_path], extractor, counts)
    
    with load(input_file) as bv:
        print("Loaded file into Binary Ninja")


    function_data = {}
    for rule_name, match_list in capabilities.matches.items():
        for match in match_list:
            feature_str = str(match[0])
            m = re.search(r'0x[0-9a-fA-F]+', feature_str)
            if not m:
                continue  # Skip if no address
            addr_str = m.group(0)
            addr_int = int(addr_str, 16)

            # Use Binary Ninja to find the function containing this address.
            funcs = bv.get_functions_containing(addr_int)
            if not funcs:
                continue 
            
            # For simplicity, choose the first function if there are several.
            func = funcs[0]
            func_name = func.name

            # If the function has not been seen, add it's disassembly
            if func_name not in function_data:
                disasm_lines = []
                for block in func.basic_blocks:
                    for line in block.disassembly_text:
                        disasm_lines.append(str(line))

                function_data[func_name] = {
                    "address": hex(func.start),
                    "rules": set(),  # We'll use a set to avoid duplicates.
                    "disassembly": disasm_lines,
                }

            # Add the rule name to the function's rule set.
            function_data[func_name]["rules"].add(rule_name)

    #Convert the rule matches for each function to a list
    for func in function_data:
        function_data[func]["rules"] = list(function_data[func]["rules"])
    
    output_dir = "matched_functions"
    os.makedirs(output_dir, exist_ok=True)

    for func_name, data in function_data.items():
        output_file = os.path.join(output_dir, f"{func_name}.json")
        with open(output_file, "w") as out_file:
            json.dump(data, out_file, indent=2)
    
    print(f"Matched functions stored in {output_dir}/")


# ------------------------------------------------------------------------------------------------------------
# Script Start
# ------------------------------------------------------------------------------------------------------------
#Loads user-specified file
input_file = get_input_file()


# Make output folder
# output_folder = "debugging_artifacts"
# os.makedirs(output_folder, exist_ok=True)

# Run analysis
capa_analyze(input_file)