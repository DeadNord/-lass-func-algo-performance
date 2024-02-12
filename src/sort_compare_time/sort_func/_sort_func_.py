import timeit
import random
import matplotlib.pyplot as plt


# Sorting Algorithms
def merge_sort(arr):
    """Perform merge sort on a list."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        merge(arr, left_half, right_half)


def merge(arr, left_half, right_half):
    """Merge two halves of a list."""
    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1


def insertion_sort(arr):
    """Perform insertion sort on a list."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def tim_sort(arr):
    """Utilize Python's built-in sort (TimSort) on a list."""
    arr.sort()


# Utility Functions
def generate_random_data(size):
    """Generate a list of random integers."""
    return [random.randint(1, 1000) for _ in range(size)]


def run_sorting_algorithm(algorithm, size):
    """Run a sorting algorithm and measure its execution time."""
    setup_code = f"from _sort_func_ import {algorithm}, generate_random_data"
    stmt = f"data = generate_random_data({size}); data_copy = data.copy(); {algorithm}(data_copy)"
    # Use timeit to measure execution time
    times = timeit.repeat(stmt, setup=setup_code, number=10, repeat=3)
    return min(times)  # Return the best time to minimize variability


def display_results(results, data_sizes):
    """Display a plot comparing the performance of different sorting algorithms."""
    for algorithm, times in results.items():
        plt.plot(data_sizes, times, label=algorithm)
    plt.xlabel("Data Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Sorting Algorithm Performance")
    plt.legend()
    plt.show()


# Main Function
def main(data_sizes, show_results=True, return_results=False):
    """Compare the performance of various sorting algorithms across different data sizes."""
    algorithms = {
        "Merge Sort": merge_sort,
        "Insertion Sort": insertion_sort,
        "TimSort": tim_sort,
    }

    results = {alg: [] for alg in algorithms}

    for size in data_sizes:
        for alg_name, alg_func in algorithms.items():
            execution_time = run_sorting_algorithm(alg_func.__name__, size)
            results[alg_name].append(execution_time)

    if show_results:
        display_results(results, data_sizes)
    if return_results:
        return results


# Execute if this is the main module
if __name__ == "__main__":
    data_sizes = [100, 500, 1000, 3000]
    main(data_sizes)
