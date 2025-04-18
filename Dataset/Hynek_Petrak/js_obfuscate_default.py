import os
import re
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# dependency
libraries = {
    "angular": [r'\bangular\b', r'import .*angular', r'require\(.*angular.*\)'],
    "bootstrap": [r'bootstrap', r'import .*bootstrap', r'require\(.*bootstrap.*\)'],
    "jquery": [r'\$', r'jQuery', r'import .*jquery', r'require\(.*jquery.*\)'],
    "electron": [r'\belectron\b', r'import .*electron', r'require\(.*electron.*\)'],
    "react": [r'\breact\b', r'import .*react', r'require\(.*react.*\)'],
}

# check dependency
def has_dependency(js_path):
    with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        for patterns in libraries.values():
            for pattern in patterns:
                if re.search(pattern, content):
                    return True
    return False

# collect all wasm files in a set (basenames without extension)
def collect_wasm_files(wasm_base_directory):
    wasm_files = set()
    for root, _, files in os.walk(wasm_base_directory):
        for file in files:
            if file.endswith(".wasm"):
                basename = os.path.splitext(file)[0]
                wasm_files.add(basename)
    return wasm_files

# obfuscate single file
def obfuscate_file(js_path, obfuscated_output):
    if os.path.exists(obfuscated_output):
        return f"Skipping {os.path.basename(js_path)} (already obfuscated)"
    os.makedirs(os.path.dirname(obfuscated_output), exist_ok=True)
    obfuscate_cmd = f'javascript-obfuscator "{js_path}" --output "{obfuscated_output}"'
    subprocess.run(obfuscate_cmd, shell=True, executable='/bin/bash')
    return f"Obfuscated {os.path.basename(js_path)}"

# process all JS files
def process_js_files(base_directory, wasm_directories, obfuscated_output_base, max_workers=30):
    #wasm file names with no .wasm
    wasm_basenames = set()
    for wasm_dir in wasm_directories:
        wasm_basenames.update(collect_wasm_files(wasm_dir))

    tasks = []

    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".js"):
                filename_wo_ext = os.path.splitext(file)[0]

                # obfuscate if there exists corresponding wasm
                if filename_wo_ext not in wasm_basenames:
                    continue

                js_path = os.path.join(root, file)

                # dependency
                if has_dependency(js_path):
                    output_dir = os.path.join(obfuscated_output_base, "With_dependency")
                else:
                    output_dir = obfuscated_output_base

                obfuscated_output = os.path.join(output_dir, filename_wo_ext + "_obfuscated.js")
                tasks.append((js_path, obfuscated_output))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(obfuscate_file, js, out) for js, out in tasks]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Obfuscating..."):
            f.result()  #messages

    print("Done")

# directories
script_directory = os.getcwd()
base_input_directory = os.path.join(script_directory, "Javascript")
wasm_dirs = [
    os.path.join(script_directory, "Wasm_Petrak"),
    os.path.join(script_directory, "Wasm_Petrak", "With_dependency"),
]
obfuscated_output_directory = os.path.join(script_directory, "Binary_obfuscated")

# let's go
process_js_files(base_input_directory, wasm_dirs, obfuscated_output_directory)

