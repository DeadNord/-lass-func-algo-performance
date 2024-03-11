// Функция оценки сложности алгоритма
function estimateComplexity(sizes, times) {
  const logSizes = sizes.map((size) => Math.log(size));
  const logTimes = times.map((time) => Math.log(time));
  const slope =
    (logTimes[logTimes.length - 1] - logTimes[0]) /
    (logSizes[logSizes.length - 1] - logSizes[0]);

  if (Math.abs(slope) < 0.1) return "O(1) - Constant complexity";
  else if (slope < 0.5) return "O(log n) - Logarithmic complexity";
  else if (slope < 1.5) return "O(n log n) - Linearithmic complexity";
  else if (Math.abs(slope - 2) < 0.5) return "O(n^2) - Quadratic complexity";
  else return "Higher complexity";
}

// Основная функция
async function main(dataSizes) {
  // Предполагаем, что данные функции и классы заранее определены
  const { sortFunc } = require("./SortFunc/sortFunc.js");
  const { SortClasses } = require("./SortClasses/sortClasses.js");

  // Получаем результаты сортировки
  const sortFuncResults = sortFunc(dataSizes, false, true);
  const sortClasses = new SortClasses(dataSizes);
  const sortClassesResults = sortClasses.run(false, true);

  const algorithms = ["Merge Sort", "Insertion Sort", "TimSort"];

  // Обрабатываем результаты для каждого алгоритма
  algorithms.forEach((alg) => {

    // Отображаем результаты в табличном формате
    console.log(`Results for ${alg}:`);
    console.log(
      "Data Size | Sort Function Time | Sort Classes Time | Percentage Increase | Speedup Factor | Absolute Time Savings (s)"
    );
    dataSizes.forEach((size, i) => {
      const funcTime = sortFuncResults[alg][i];
      const classTime = sortClassesResults[alg][i];
      const percentageIncrease = ((funcTime - classTime) / classTime) * 100;
      const speedupFactor = funcTime / classTime;
      const absoluteTimeSavings = funcTime - classTime;

      console.log(
        `${size} | ${funcTime.toFixed(4)} | ${classTime.toFixed(
          4
        )} | ${percentageIncrease.toFixed(2)}% | ${speedupFactor.toFixed(
          2
        )} | ${absoluteTimeSavings.toFixed(4)}`
      );
    });

    // Оцениваем сложность алгоритма
    const funcComplexity = estimateComplexity(dataSizes, sortFuncResults[alg]);
    const classComplexity = estimateComplexity(
      dataSizes,
      sortClassesResults[alg]
    );
    console.log(`Functional Complexity: ${funcComplexity}`);
    console.log(`Class-based Complexity: ${classComplexity}`);
  });
}

// Запускаем основную функцию
main([10, 20, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800]);
