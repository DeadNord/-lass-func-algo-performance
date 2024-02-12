from tabulate import tabulate
import matplotlib.pyplot as plt
import sys
import importlib.util

data_sizes = [100, 500, 1000, 3000]

# Sort Function
module_path = "src/sort_compare_time/sort_func"
if module_path not in sys.path:
    sys.path.append(module_path)
sort_func_module = importlib.import_module("_sort_func_")
sort_func = sort_func_module.main
sort_func_results = sort_func(data_sizes)

# Sort Classes
module_path = "src/sort_compare_time/sort_classes"
if module_path not in sys.path:
    sys.path.append(module_path)
sort_classes_module = importlib.import_module("_sort_classes_")
SortClasses = sort_classes_module.MainProgram(data_sizes)
sort_classes_results = SortClasses.run(show_results=False, return_results=True)

algorithms = ["Merge Sort", "Insertion Sort", "TimSort"]
headers = ["Data Size"] + [
    "Sort Function",
    "Sort Classes",
]

for alg in algorithms:
    table_data = []
    for i, size in enumerate(data_sizes):
        row = [size]
        row.append(sort_func_results[alg][i])
        row.append(sort_classes_results[alg][i])
        table_data.append(row)
    print(f"Results for {alg}:")
    print(tabulate(table_data, headers=headers, tablefmt="pipe"))
    print("\n")


for alg in algorithms:
    plt.figure(figsize=(10, 6))
    plt.plot(data_sizes, sort_func_results[alg], label="sort_func")
    plt.plot(data_sizes, sort_classes_results[alg], label="sort_classes")
    plt.xlabel("Data Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Comparison of {alg}")
    plt.legend()
    plt.show()
