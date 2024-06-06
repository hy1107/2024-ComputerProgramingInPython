//ch3 01
const result = 2 ** 10;
console.log(result);  // 輸出: 1024

//ch3 02
const dividend = 100;
const divisor = 7;

// 商
const quotient = Math.floor(dividend / divisor);

// 餘數
const remainder = dividend % divisor;

console.log(`商: ${quotient}`);  // 輸出: 商: 14
console.log(`餘數: ${remainder}`);  // 輸出: 餘數: 2

//ch3 03
const dividend3 = 10;
const divisor3 = 3;

// 計算除法結果
const result3 = dividend3 / divisor3;

// 保留2位小數
const formattedResult = result3.toFixed(2);

console.log(formattedResult);  // 輸出: 3.33

//ch3 04
const str4 = "5";
const num4 = parseFloat(str4);
const result4 = num4 + 10;
console.log(result4);  // 輸出: 15

//ch3 05
const radius5 = 7;
const area5 = Math.PI * Math.pow(radius5, 2);

console.log(`area: ${area5}`);

//ch3 06
const str16 = "hello";
const str26 = "world";
const result6 = `${str16}${str26}`;
console.log(result6);  // 輸出: helloworld

//ch3 07
const number7 = 123;
const unitsDigit7 = number7 % 10;
console.log(unitsDigit7);  // 輸出: 3

//ch3 08
let num8 = 4;
let result8 = String(num8) + "2";
console.log(result8);  // 輸出: "42"

//ch3 09
let num9 = 15;
let result9 = num9 >= 10 && num9 <= 20;
console.log(result9);  // 輸出: true

//ch3 10
let str10 = "hello";
let result10 = str10 !== "" && str10 !== undefined;
console.log(result10);  // 輸出: true

//ch3 11
let num11 = 25;
let result11 = (num11 % 2 === 0) ? "Even" : "Odd";
console.log(result11);  // 輸出: "Odd"

//ch3 12
let x12 = 30;
let y12 = 20;
let result12 = (x12 > y12) ? x12 : y12;
console.log(result12);  // 輸出: 30