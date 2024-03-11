import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import timeit


# Utility function to generate random data
def generate_random_data(size):
    """Generate a list of random integers."""
    return [random.randint(1, 1000) for _ in range(size)]


class TimeMeasurer:
    """Static class for measuring execution time of sorting algorithms."""

    @staticmethod
    def measure_time(func, *args, number=10, repeat=3):
        """Measures the execution time of a provided sorting function.

        Args:
            func: The sorting function to measure.
            data: The data to sort.
            number: The number of times to execute the function per trial.
            repeat: The number of trials to run.

        Returns:
            The minimum execution time measured across all trials.
        """
        timer = timeit.Timer(lambda: func(*args))
        times = timer.repeat(repeat, number)

        return min(times) / number


class SortingAlgorithm:
    """Abstract base class for sorting algorithms."""

    def sort(self, data):
        """Sort the data. Must be implemented by subclasses."""
        raise NotImplementedError("Sort function not defined")


class MergeSort(SortingAlgorithm):
    """Implements the merge sort algorithm."""

    def sort(self, data):
        if len(data) > 1:
            mid = len(data) // 2
            left, right = data[:mid], data[mid:]
            self.sort(left)
            self.sort(right)
            self._merge(data, left, right)

    def _merge(self, data, left, right):
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            data[k] = left[i]
            i, k = i + 1, k + 1
        while j < len(right):
            data[k] = right[j]
            j, k = j + 1, k + 1


class InsertionSort(SortingAlgorithm):
    """Implements the insertion sort algorithm."""

    def sort(self, arr):
        """Simple insertion sort algorithm."""
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key


class TimSort(SortingAlgorithm):
    """Wrapper for Python's built-in sort method, utilizing TimSort."""

    def sort(self, arr):
        """Python's built-in sort."""
        arr.sort()


class SortingHandler:
    """Manages sorting operations with different algorithms."""

    def __init__(self):
        self.algorithms = {
            "Merge Sort": MergeSort(),
            "Insertion Sort": InsertionSort(),
            "TimSort": TimSort(),
        }

    def perform_sorting(self, algorithm_name, data):
        """Perform sorting using the specified algorithm."""
        algorithm = self.algorithms.get(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        # Clone data to prevent in-place sorting affecting subsequent algorithms
        data_copy = data[:]
        algorithm.sort(data_copy)
        return data_copy


class ResultHandler:
    """Handles displaying and plotting of sorting algorithm performance results."""

    @staticmethod
    def display_table(data_sizes, results):
        """Display results in a table format."""
        headers = ["Data Size"] + list(results.keys())
        rows = [
            [size] + [results[algorithm][i] for algorithm in sorted(results)]
            for i, size in enumerate(data_sizes)
        ]
        print(tabulate(rows, headers=headers, tablefmt="pipe"))

    @staticmethod
    def plot_results(data_sizes, results):
        """Plots the sorting performance results."""
        for algorithm, execution_times in results.items():
            plt.plot(data_sizes, execution_times, label=algorithm)
        plt.xlabel("Data Size")
        plt.ylabel("Execution Time (seconds)")
        plt.title("Sorting Algorithm Performance Comparison")
        plt.legend()
        plt.show()


class MainProgram:
    """Coordinates the execution of sorting algorithm performance comparison."""

    def __init__(self, data_sizes):
        self.data_sizes = data_sizes
        self.sorting_handler = SortingHandler()
        self.results = {algorithm: [] for algorithm in self.sorting_handler.algorithms}

    def run(self, show_results=True, return_results=False):
        """Executes the performance comparison for the specified data sizes."""
        for size in self.data_sizes:
            data = generate_random_data(size)
            for algorithm in self.sorting_handler.algorithms:
                execution_time = TimeMeasurer.measure_time(
                    self.sorting_handler.perform_sorting, algorithm, data
                )
                self.results[algorithm].append(execution_time)

        if show_results:
            ResultHandler.display_table(self.data_sizes, self.results)
            ResultHandler.plot_results(self.data_sizes, self.results)

        if return_results:
            return self.results


# Main execution block
if __name__ == "__main__":
    data_sizes = [100, 500, 1000, 3000]
    program = MainProgram(data_sizes)
    program.run()
