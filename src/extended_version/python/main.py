from tabulate import tabulate
import matplotlib.pyplot as plt
import sys
import importlib.util
import numpy as np


def estimate_complexity(sizes, times):
    """
    Estimates the computational complexity of an algorithm based on input sizes and execution times.

    Parameters:
    - sizes: A list of input sizes.
    - times: A list of execution times corresponding to each input size.

    Returns:
    - A string representation of the estimated complexity.
    """
    # Calculate logarithms of sizes and times for linear regression
    log_sizes = np.log(sizes)
    log_times = np.log(times)

    # Perform linear regression to find the slope and intercept
    slope, intercept = np.polyfit(log_sizes, log_times, 1)

    # Interpret the slope to estimate complexity
    if np.isclose(slope, 0):
        return "O(1) - Constant complexity"
    elif 0 < slope < 0.5:
        return "O(log n) - Logarithmic complexity"
    elif 0.5 <= slope < 1.5:
        return "O(n log n) - Linearithmic complexity"
    elif np.isclose(slope, 2) or (1.5 <= slope < 2.5):
        return "O(n^2) - Quadratic complexity"
    else:
        return "Higher complexity"


def load_module(module_path, module_name):
    """
    Dynamically loads a module given its file path and module name.

    Parameters:
    - module_path: The file path to the module.
    - module_name: The name of the module to load.

    Returns:
    - The loaded module.
    """
    if module_path not in sys.path:
        sys.path.append(module_path)
    return importlib.import_module(module_name)


def plot_results(data_sizes, sort_func_results, sort_classes_results, algorithms):
    """
    Plots the execution time of sorting algorithms implemented as functions and classes.

    Parameters:
    - data_sizes: List of data sizes.
    - sort_func_results: Execution times of the function-based implementations.
    - sort_classes_results: Execution times of the class-based implementations.
    - algorithms: List of algorithm names.
    """
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


def main(data_sizes):
    """
    Main program to compare the performance and complexity of sorting algorithms implemented as functions and classes.

    Parameters:
    - data_sizes: A list of data sizes to test the algorithms with.
    """
    # Load sorting function and classes from external modules
    sort_func = load_module("src/sort_compare_time/sort_func", "_sort_func_").main
    SortClasses = load_module(
        "src/sort_compare_time/sort_classes", "_sort_classes_"
    ).MainProgram(data_sizes)

    # Execute sorting and collect results
    sort_func_results = sort_func(data_sizes, show_results=False, return_results=True)
    sort_classes_results = SortClasses.run(show_results=False, return_results=True)

    # Define the algorithms to compare
    algorithms = ["Merge Sort", "Insertion Sort", "TimSort"]
    headers = [
        "Data Size",
        "Sort Function Time",
        "Sort Classes Time",
        "Percentage Increase",
        "Speedup Factor",
        "Absolute Time Savings (s)",
    ]

    # Process results for each algorithm
    for alg in algorithms:
        table_data = []
        cost_per_element_table = []

        for i, size in enumerate(data_sizes):
            func_time = sort_func_results[alg][i]
            class_time = sort_classes_results[alg][i]
            percentage_increase = (
                ((func_time - class_time) / class_time) * 100 if class_time != 0 else 0
            )
            speedup_factor = func_time / class_time if class_time != 0 else float("inf")
            absolute_time_savings = func_time - class_time
            cost_per_element_func = func_time / size
            cost_per_element_class = class_time / size

            table_data.append(
                [
                    size,
                    func_time,
                    class_time,
                    f"{percentage_increase:.2f}%",
                    f"{speedup_factor:.2f}",
                    f"{absolute_time_savings:.2e}",
                ]
            )
            cost_per_element_table.append(
                [size, f"{cost_per_element_func:.2e}", f"{cost_per_element_class:.2e}"]
            )

        func_complexity = estimate_complexity(data_sizes, sort_func_results[alg])
        class_complexity = estimate_complexity(data_sizes, sort_classes_results[alg])

        # Display results in a tabular format
        print(f"\nResults for {alg}:")
        print(tabulate(table_data, headers=headers, tablefmt="pipe"))
        print(f"\nCost per Element for {alg}:")
        print(
            tabulate(
                cost_per_element_table,
                headers=[
                    "Data Size",
                    "Cost per Element (Func)",
                    "Cost per Element (Class)",
                ],
                tablefmt="pipe",
            )
        )
        print(f"\nComplexity for {alg}:")
        print(f"Functional Complexity: {func_complexity}")
        print(f"Class-based Complexity: {class_complexity}\n")

    # Plot results
    plot_results(data_sizes, sort_func_results, sort_classes_results, algorithms)


if __name__ == "__main__":
    # data_sizes = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000]
    data_sizes = [10, 20, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800]
    main(data_sizes)
