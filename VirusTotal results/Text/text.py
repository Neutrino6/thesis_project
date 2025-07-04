import os
import json
from collections import defaultdict

def count_categories_in_folder(folder_path):
    
    categories = ["malicious", "suspicious", "harmless"]
    category_counts = {cat: defaultdict(int) for cat in categories}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue

        full_path = os.path.join(folder_path, filename)
        with open(full_path, "r") as f:
            try:
                data = json.load(f)
                results = data["data"]["attributes"]["results"]

                # Count antiviruses for the given category
                for cat in categories:
                    count = sum(1 for v in results.values() if v.get("category") == cat)
                    category_counts[cat][count] += 1

            except Exception as e:
                print(f"Error in {filename}: {e}")

    
    for cat in categories:
        category_counts[cat] = dict(sorted(category_counts[cat].items()))

    return category_counts

# Folders
folders = ["vt_wasm", "vt_wasm_obf_js_obf", "vt_wasm_js_obf", "vt_wasm_obf"]

for folder in folders:
    category_counts = count_categories_in_folder(folder)
    output_filename = f"stat_{folder}.txt"

    with open(output_filename, "w") as out_file:
        out_file.write(f"Results for {folder}:\n\n")

        for category, counts in category_counts.items():
            out_file.write(f"Category: {category}\n")
            for vendor_count, file_count in counts.items():
                out_file.write(f"{file_count} files have been marked by {vendor_count} antiviruses \n")
            out_file.write("\n")

    print(f"Saved in {output_filename}")


