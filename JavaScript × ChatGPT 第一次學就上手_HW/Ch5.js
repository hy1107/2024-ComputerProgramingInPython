//CH5-1
//(1) 寫一個函式用來計算任意數字的平均值
function calculateAverage(numbers) {
    if (numbers.length === 0) {
        return 0; // 如果沒有數字，平均值為 0
    }

    var sum = 0;
    for (var i = 0; i < numbers.length; i++) {
        sum += numbers[i]; // 將數字加總
    }

    return sum / numbers.length; // 回傳平均值
}

// 範例用法
var numbers = [1, 2, 3, 4, 5];
var average = calculateAverage(numbers);
console.log("平均值為: " + average);

//(2) 寫一個函式用來檢查一個數字是否為質數
function isPrime(number) {
    // 質數必須大於 1
    if (number <= 1) {
        return false;
    }

    // 檢查是否有除了 1 和自身以外的因數
    for (var i = 2; i <= Math.sqrt(number); i++) {
        if (number % i === 0) {
            return false; // 如果能被整除，不是質數
        }
    }

    return true; // 如果沒有除了 1 和自身以外的因數，是質數
}

// 範例用法
var number = 13;
if (isPrime(number)) {
    console.log(number + " 是質數");
} else {
    console.log(number + " 不是質數");
}

//(3) 寫一個函式用來將一個數字轉換為其二進位表示法的字串
function decimalToBinary(number) {
    // 使用toString方法轉換為二進位字串
    return number.toString(2);
}

// 範例用法
var number = 10;
var binaryString = decimalToBinary(number);
console.log(number + " 的二進位表示法為: " + binaryString);

//(4) 寫一個函式用來找出陣列中的最小值與最大值
function findMinAndMax(array) {
    if (array.length === 0) {
        return { min: undefined, max: undefined };
    }

    var min = array[0];
    var max = array[0];

    for (var i = 1; i < array.length; i++) {
        if (array[i] < min) {
            min = array[i];
        }
        if (array[i] > max) {
            max = array[i];
        }
    }

    return { min: min, max: max };
}

// 範例用法
var numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5];
var result = findMinAndMax(numbers);
console.log("最小值: " + result.min);
console.log("最大值: " + result.max);

//CH5-2
//(1) 寫一個遞迴函式來計算費氏數列中的第n項
function fibonacci(n) {
    if (n <= 1) {
        return n; // 基本情況，n=0或n=1時，返回n
    } else {
        // 遞迴情況，返回前兩項費氏數列的和
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// 範例用法
var n = 6;
var result = fibonacci(n);
console.log("費氏數列中第 " + n + " 項為: " + result);

//(2) 寫一個遞迴函式來計算兩個正整數的最大公因數(GCD)
function gcd(a, b) {
    // 如果其中一個數為0，則另一個數為最大公因數
    if (b === 0) {
        return a;
    } else {
        // 否則，遞迴計算較小的數和兩數相除的餘數的最大公因數
        return gcd(b, a % b);
    }
}

// 範例用法
var num1 = 36;
var num2 = 24;
var result = gcd(num1, num2);
console.log("最大公因數為: " + result);