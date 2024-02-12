from tabulate import tabulate
import matplotlib.pyplot as plt
import sys
import importlib.util
import numpy as np


def estimate_complexity(sizes, times):
    log_sizes = np.log(sizes)
    log_times = np.log(times)
    coefficients = np.polyfit(log_sizes, log_times, 1)
    slope, intercept = coefficients

    # Adjust these conditions based on observed data and theoretical expectations
    if np.isclose(slope, 0):
        return "O(1) - Constant complexity"
    elif slope > 0 and slope < 0.5:
        return "O(log n) - Logarithmic complexity"
    elif slope >= 0.5 and slope < 1.5:
        return "O(n log n) - Linearithmic complexity"
    elif np.isclose(slope, 2) or (slope >= 1.5 and slope < 2.5):
        return "O(n^2) - Quadratic complexity"
    else:
        return "Higher complexity"


def main(data_sizes):
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
    headers = ["Data Size", "Sort Function", "Sort Classes"]

    for alg in algorithms:
        table_data = []
        for i, size in enumerate(data_sizes):
            row = [size]
            row.append(sort_func_results[alg][i])
            row.append(sort_classes_results[alg][i])
            table_data.append(row)

        # Estimate complexities here (moved inside the loop for direct access)
        func_complexity = estimate_complexity(data_sizes, sort_func_results[alg])
        class_complexity = estimate_complexity(data_sizes, sort_classes_results[alg])

        print(f"\nResults for {alg}:")
        print(tabulate(table_data, headers=headers, tablefmt="pipe"))
        print(f"Functional Complexity: {func_complexity}")
        print(f"Class-based Complexity: {class_complexity}\n")

    for alg in algorithms:
        plt.figure(figsize=(10, 6))
        plt.plot(data_sizes, sort_func_results[alg], label="Functional Implementation")
        plt.plot(
            data_sizes, sort_classes_results[alg], label="Class-based Implementation"
        )
        plt.xlabel("Data Size")
        plt.ylabel("Execution Time (seconds)")
        plt.title(f"Comparison of {alg}")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # data_sizes = [100, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    data_sizes = [100, 500, 1000]
    main(data_sizes)
