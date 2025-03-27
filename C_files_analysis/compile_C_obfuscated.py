import os
import subprocess

def compile_obfuscated_c_files(directory, output_directory):
    
    c_files = [f for f in os.listdir(directory) if f.endswith("_tigress.c")]
    
    if not c_files:
        print("No file _tigress.c in the directory")
        return
        
        
    #creates output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
        
        
    for c_file in c_files:
        #take the name
        c_file_name = os.path.basename(c_file)
        
        #rename
        output_file = c_file_name.replace("_tigress.c", "") + "_native_obfuscated"
        
        
        #path for the output
        output_file_path = os.path.join(output_directory, output_file)
        
        
        #create command
        gcc_command = f' gcc {c_file_name} -o {output_file_path}'
        
        #compile the file
        print(f"Compile {c_file_name} with gcc")
        subprocess.run(gcc_command, shell=True, executable='/bin/bash', cwd=directory)
    
    print("Completed")

#take current directory path
script_directory = os.getcwd()

source_directory = os.path.join(script_directory, "C_obfuscated")
output_directory = os.path.join(script_directory, "native_obfuscated")

#compile
compile_obfuscated_c_files(source_directory, output_directory)


