const { performance } = require("perf_hooks");


function merge(arr, leftHalf, rightHalf) {
  let i = 0,
    j = 0,
    k = 0;
  while (i < leftHalf.length && j < rightHalf.length) {
    if (leftHalf[i] < rightHalf[j]) {
      arr[k++] = leftHalf[i++];
    } else {
      arr[k++] = rightHalf[j++];
    }
  }

  while (i < leftHalf.length) arr[k++] = leftHalf[i++];
  while (j < rightHalf.length) arr[k++] = rightHalf[j++];
}

// Sorting Algorithms
function mergeSort(arr) {
  if (arr.length > 1) {
    const mid = Math.floor(arr.length / 2);
    const leftHalf = arr.slice(0, mid);
    const rightHalf = arr.slice(mid);

    mergeSort(leftHalf);
    mergeSort(rightHalf);

    merge(arr, leftHalf, rightHalf);
  }
}


function insertionSort(arr) {
  for (let i = 1; i < arr.length; i++) {
    let key = arr[i];
    let j = i - 1;
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
}

function timSort(arr) {
  arr.sort((a, b) => a - b);
}

// Utility Functions
function generateRandomData(size) {
  const data = [];
  for (let i = 0; i < size; i++) {
    data.push(Math.floor(Math.random() * 1000) + 1);
  }
  return data;
}

function runSortingAlgorithm(algorithm, size) {
  const data = generateRandomData(size);
  const start = performance.now();
  algorithm(data);
  const end = performance.now();
  return (end - start) / 1000; // Return time in seconds
}

// Omitting direct plotting in JavaScript, but you can log results or use them with a chart library
function displayResults(results, dataSizes) {
  console.log("Sorting Algorithm Performance:");
  for (const [algorithm, times] of Object.entries(results)) {
    console.log(`${algorithm}:`);
    dataSizes.forEach((size, index) => {
      console.log(`Data Size ${size}: ${times[index].toFixed(4)} seconds`);
    });
  }
}

// Main Function
function main(dataSizes, showResults = true, returnResults = false) {
  const algorithms = {
    "Merge Sort": mergeSort,
    "Insertion Sort": insertionSort,
    TimSort: timSort,
  };

  const results = {};

  for (const algName in algorithms) {
    const algFunc = algorithms[algName];
    results[algName] = [];
    for (const size of dataSizes) {
      const executionTime = runSortingAlgorithm(algFunc, size);
      results[algName].push(executionTime);
    }
  }

  if (showResults) {
    displayResults(results, dataSizes);
  }
  if (returnResults) {
    return results;
  }
}

// Execute if this script is run directly
if (require.main === module) {
  const dataSizes = [100, 500, 1000, 3000];
  main(dataSizes);
}

module.exports = {
  sortFunc: main
};
