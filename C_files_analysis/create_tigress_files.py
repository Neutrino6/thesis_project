import os
import subprocess

def obfuscate_c_files(input_directory, output_directory):
    c_files = [f for f in os.listdir(input_directory) if f.endswith(".c")]
    
    if not c_files:
        print("No C file in the directory")
        return
    
    #create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for c_file in c_files:
        c_path = os.path.join(input_directory, c_file)
        output_file = os.path.splitext(c_file)[0] + "_tigress.c"
        
        #output path
        output_file_path = os.path.join(output_directory, output_file)
        
        #tigress command
        tigress_command = f'./tigress --Environment=x86_64:Linux:Gcc:13.1 --Transform=Flatten --Functions=main --out={output_file_path} {c_file}'
        
        
        print(f"Obfuscating {c_file}...")
        subprocess.run(tigress_command, shell=True, executable='/bin/bash', cwd=input_directory)
    
    print("Obfuscation completed")

#take tigress directory
input_directory = input("Enter the full path to the Tigress directory (e.g., /path/to/tigress/3.3.3). The files must be inside that directory: ")

#this path
script_directory = os.getcwd()

#output path
output_directory = os.path.join(script_directory, "C_obfuscated")

#obfuscate
obfuscate_c_files(input_directory, output_directory)


