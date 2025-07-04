import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns


def count_categories_in_folder(folder_path):
    categories = ["malicious", "suspicious", "harmless"]
    category_counts = {cat: defaultdict(int) for cat in categories}
    all_file_counts = {cat: [] for cat in categories}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue

        full_path = os.path.join(folder_path, filename)
        with open(full_path, "r") as f:
            try:
                data = json.load(f)
                results = data["data"]["attributes"]["results"]

                for cat in categories:
                    count = sum(1 for v in results.values() if v.get("category") == cat)
                    category_counts[cat][count] += 1
                    all_file_counts[cat].append(count)

            except Exception as e:
                print(f"Errore nel file {filename}: {e}")

    for cat in categories:
        category_counts[cat] = dict(sorted(category_counts[cat].items()))

    return category_counts, all_file_counts


folders = ["vt_wasm", "vt_wasm_obf_js_obf", "vt_wasm_js_obf", "vt_wasm_obf"]


folder_names = []
all_malicious_distributions = []

for folder in folders:
    category_counts, filewise_counts = count_categories_in_folder(folder)
    
    # data for boxplot
    folder_names.append(folder)
    all_malicious_distributions.append(filewise_counts["malicious"])

# boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=all_malicious_distributions)
plt.xticks(ticks=range(len(folder_names)), labels=folder_names, rotation=15)
plt.ylabel("Number of antiviruses which mark as 'malicious'")
plt.title("Distribution of detections by folder")
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("boxplot_malicious.png")
plt.show()
