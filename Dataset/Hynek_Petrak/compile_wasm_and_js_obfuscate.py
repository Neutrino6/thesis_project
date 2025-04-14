import os
import re
import subprocess

#dependency
libraries = {
    "angular": [r'\bangular\b', r'import .*angular', r'require\(.*angular.*\)'],
    "bootstrap": [r'bootstrap', r'import .*bootstrap', r'require\(.*bootstrap.*\)'],
    "jquery": [r'\$', r'jQuery', r'import .*jquery', r'require\(.*jquery.*\)'],
    "electron": [r'\belectron\b', r'import .*electron', r'require\(.*electron.*\)'],
    "react": [r'\breact\b', r'import .*react', r'require\(.*react.*\)'],
}

#check dependency
def has_dependency(js_path):
    with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        for patterns in libraries.values():
            for pattern in patterns:
                if re.search(pattern, content):
                    return True
    return False

#compile in wasm with javy, and obfuscate javascript
def process_js_files(base_directory, wasm_output_base, obfuscated_output_base):
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".js"):
                js_path = os.path.join(root, file)
                filename_wo_ext = os.path.splitext(file)[0]

                #dependency
                has_dep = has_dependency(js_path)

                #output directories
                wasm_subdir = "With_dependency" if has_dep else ""
                wasm_output_dir = os.path.join(wasm_output_base, wasm_subdir)
                os.makedirs(wasm_output_dir, exist_ok=True)

                wasm_output_path = os.path.join(wasm_output_dir, filename_wo_ext + ".wasm")

                #javy
                compile_cmd = f'./javy build "{js_path}" -o "{wasm_output_path}"'
                print(f"Compiling {file} -> {wasm_output_path}")
                subprocess.run(compile_cmd, shell=True, executable='/bin/bash')

                #javascript-obfuscator
                os.makedirs(obfuscated_output_base, exist_ok=True)
                obfuscated_output = os.path.join(obfuscated_output_base, filename_wo_ext + "_obfuscated.js")
                obfuscate_cmd = f'javascript-obfuscator "{js_path}" --output "{obfuscated_output}"'
                print(f"Obfuscating {file} -> {obfuscated_output}")
                subprocess.run(obfuscate_cmd, shell=True, executable='/bin/bash')

    print("Operazione completata.")

#directories
script_directory = os.getcwd()
base_input_directory = os.path.join(script_directory, "Javascript")
wasm_output_directory = os.path.join(script_directory, "Wasm_Petrak")
obfuscated_output_directory = os.path.join(script_directory, "Binary_obfuscated")

#let's go
process_js_files(base_input_directory, wasm_output_directory, obfuscated_output_directory)

