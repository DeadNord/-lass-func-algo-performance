import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import timeit


# TimeMeasurer: Static class for measuring execution time of a function
class TimeMeasurer:
    @staticmethod
    def measure_time(func, *args, number=10, repeat=3):
        """Measure the execution time of a function using timeit.repeat().

        Args:
            func (callable): The function to measure.
            *args: Arguments to pass to the function.
            number (int): How many times to call the function in each repeat.
            repeat (int): How many times to repeat the timer (default 3).

        Returns:
            float: The best time from the repeats.
        """
        timer = timeit.Timer(lambda: func(*args))
        times = timer.repeat(repeat, number)
        best_time = min(times) / number

        return best_time


# SortingAlgorithm: Base class for sorting algorithms
class SortingAlgorithm:
    def sort(self, data):
        """Sort the data. Must be implemented by subclasses."""
        raise NotImplementedError("Sort function not defined")


# MergeSort: Implements the merge sort algorithm
class MergeSort(SortingAlgorithm):
    def sort(self, arr):
        """Recursive merge sort algorithm."""
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            self.sort(left_half)
            self.sort(right_half)

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


# InsertionSort: Implements the insertion sort algorithm
class InsertionSort(SortingAlgorithm):
    def sort(self, arr):
        """Simple insertion sort algorithm."""
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key


# TimSort: Utilizes Python's built-in sort, which is based on TimSort
class TimSort(SortingAlgorithm):
    def sort(self, arr):
        """Python's built-in sort."""
        arr.sort()


# SortingHandler: Manages sorting operations with different algorithms
class SortingHandler:
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


# ResultHandler: Handles displaying and plotting of results
class ResultHandler:
    @staticmethod
    def display_table(data_sizes, results):
        """Display results in a table format."""
        headers = ["Data Size"] + list(results.keys())
        table_data = [
            [size] + [results[algorithm][i] for algorithm in results]
            for i, size in enumerate(data_sizes)
        ]
        print(tabulate(table_data, headers=headers, tablefmt="pipe"))

    @staticmethod
    def plot_results(data_sizes, results):
        """Plot the results of sorting algorithm comparisons."""
        for algorithm, execution_times in results.items():
            plt.plot(data_sizes, execution_times, label=algorithm)
        plt.xlabel("Data Size")
        plt.ylabel("Execution Time (seconds)")
        plt.title("Sorting Algorithm Comparison")
        plt.legend()
        plt.show()


# MainProgram: Coordinates the execution of the sorting algorithm comparison
class MainProgram:
    def __init__(self, data_sizes):
        self.sorter = SortingHandler()
        self.data_sizes = data_sizes
        self.results = {alg: [] for alg in self.sorter.algorithms}

    def run(self, show_results=True, return_results=False):
        """Execute the sorting comparison for different data sizes."""
        for size in self.data_sizes:
            data = generate_random_data(size)

            for title in self.sorter.algorithms:
                execution_time = TimeMeasurer.measure_time(
                    self.sorter.perform_sorting, title, data.copy()
                )
                self.results[title].append(execution_time)

        if show_results:
            ResultHandler.display_table(self.data_sizes, self.results)
            ResultHandler.plot_results(self.data_sizes, self.results)

        if return_results:
            return self.results


# Utility function to generate random data
def generate_random_data(size):
    """Generate a list of random integers."""
    return [random.randint(1, 1000) for _ in range(size)]


# Main execution block
if __name__ == "__main__":
    data_sizes = [100, 500, 1000, 3000]
    program = MainProgram(data_sizes)
    program.run()
