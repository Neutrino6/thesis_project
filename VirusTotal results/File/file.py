import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def count_categories_in_folder(folder_path):
    categories = ["malicious", "suspicious", "harmless"]
    category_counts = {cat: defaultdict(int) for cat in categories}

    total_files = 0
    malicious_files = 0
    malicious_5plus_files = 0

    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue

        full_path = os.path.join(folder_path, filename)
        with open(full_path, "r") as f:
            try:
                data = json.load(f)
                results = data["data"]["attributes"]["results"]
                total_files += 1

                # count malicious files
                malicious_count = 0
                for cat in categories:
                    count = sum(1 for v in results.values() if v.get("category") == cat)
                    category_counts[cat][count] += 1
                    if cat == "malicious":
                        malicious_count = count

                if malicious_count >= 1:
                    malicious_files += 1
                if malicious_count >= 5:
                    malicious_5plus_files += 1

            except Exception as e:
                print(f"Error in {filename}: {e}")

    for cat in categories:
        category_counts[cat] = dict(sorted(category_counts[cat].items()))

    return category_counts, total_files, malicious_files, malicious_5plus_files


folders = ["vt_wasm", "vt_wasm_obf_js_obf", "vt_wasm_js_obf", "vt_wasm_obf"]

for folder in folders:
    category_counts, total, malicious, malicious_5plus = count_categories_in_folder(folder)

    perc_malicious = (malicious / total * 100) if total > 0 else 0.0
    perc_malicious_5plus = (malicious_5plus / total * 100) if total > 0 else 0.0

    for category, counts in category_counts.items():
        x = list(counts.keys())       # number of vendors
        y = list(counts.values())     # number of files

        plt.figure(figsize=(10, 5))
        color = "darkred" if category == "malicious" else "orange" if category == "suspicious" else "gray"
        plt.bar(x, y, color=color)
        plt.xlabel("Number of antiviruses")
        plt.ylabel("Number of files")
        
        
        title = (
            f"{folder} - {category.upper()} | "
            f"{perc_malicious:.2f}% malicious (≥1 Antiviruses) | "
            f"{perc_malicious_5plus:.2f}% malicious (≥5 Antiviruses)"
        )
        plt.title(title)
        plt.xticks(x)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()
        
        safe_folder = folder.replace("/", "_")
        output_path = f"{safe_folder}__{category}.png"
        plt.savefig(output_path)
        plt.close()
