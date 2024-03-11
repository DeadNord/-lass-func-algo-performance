const { performance } = require('perf_hooks');

// Utility function to generate random data
function generateRandomData(size) {
  const data = [];
  for (let i = 0; i < size; i++) {
    data.push(Math.floor(Math.random() * 1000) + 1);
  }
  return data;
}

class SortingAlgorithm {
  sort(data) {
    throw new Error('Method not implemented.');
  }
}

class MergeSort extends SortingAlgorithm {
  sort(data) {
    if (data.length > 1) {
      const mid = Math.floor(data.length / 2);
      const left = data.slice(0, mid);
      const right = data.slice(mid);
      this.sort(left);
      this.sort(right);
      this.merge(data, left, right);
    }
  }

  merge(data, left, right) {
    let i = 0,
      j = 0,
      k = 0;
    while (i < left.length && j < right.length) {
      if (left[i] < right[j]) {
        data[k++] = left[i++];
      } else {
        data[k++] = right[j++];
      }
    }
    while (i < left.length) data[k++] = left[i++];
    while (j < right.length) data[k++] = right[j++];
  }
}

class InsertionSort extends SortingAlgorithm {
  sort(data) {
    for (let i = 1; i < data.length; i++) {
      let key = data[i];
      let j = i - 1;
      while (j >= 0 && data[j] > key) {
        data[j + 1] = data[j];
        j = j - 1;
      }
      data[j + 1] = key;
    }
  }
}

class TimSort extends SortingAlgorithm {
  sort(data) {
    data.sort((a, b) => a - b);
  }
}

class SortingHandler {
  constructor() {
    this.algorithms = {
      'Merge Sort': new MergeSort(),
      'Insertion Sort': new InsertionSort(),
      'TimSort': new TimSort(),
    };
  }

  performSorting(algorithmName, data) {
    const algorithm = this.algorithms[algorithmName];
    if (!algorithm) {
      throw new Error(`Algorithm ${algorithmName} not found`);
    }
    const dataCopy = [...data];
    algorithm.sort(dataCopy);
    return dataCopy;
  }
}

class TimeMeasurer {
  static measureTime(func, args, number = 10, repeat = 3) {
    const times = [];
    for (let i = 0; i < repeat; i++) {
      const start = performance.now();
      for (let j = 0; j < number; j++) {
        func(...args);
      }
      const end = performance.now();
      times.push((end - start) / number);
    }
    return Math.min(...times);
  }
}

class MainProgram {
  constructor(dataSizes) {
    this.dataSizes = dataSizes;
    this.sortingHandler = new SortingHandler();
    this.results = {};
    Object.keys(this.sortingHandler.algorithms).forEach(algorithm => {
      this.results[algorithm] = [];
    });
  }

  run(showResults = true, returnResults = false) {
    for (const size of this.dataSizes) {
      const data = generateRandomData(size);
      Object.keys(this.sortingHandler.algorithms).forEach(algorithm => {
        const executionTime = TimeMeasurer.measureTime(
          this.sortingHandler.performSorting.bind(this.sortingHandler),
          [algorithm, data]
        );
        this.results[algorithm].push(executionTime);
      });
    }

    if (showResults) {
      this.displayResults();
    }

    if (returnResults) {
      return this.results;
    }
  }

  displayResults() {
    console.log('Sorting Performance Results:');
    Object.entries(this.results).forEach(([algorithm, times]) => {
      console.log(`\n${algorithm}:`);
      times.forEach((time, index) => {
        console.log(`Data Size ${this.dataSizes[index]}: ${time.toFixed(4)} seconds`);
      });
    });
  }
}

// Main execution block
// const dataSizes = [100, 500, 1000, 3000];
// const program = new MainProgram(dataSizes);
// program.run();

module.exports = {
  SortClasses: MainProgram
};
