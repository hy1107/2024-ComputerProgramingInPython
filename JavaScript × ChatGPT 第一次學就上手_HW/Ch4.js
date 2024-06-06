//ch4 01
let year041 = prompt("請輸入年份:");
let isLeapYear041 = (year041 % 4 === 0 && year041 % 100 !== 0) || (year041 % 400 === 0);
console.log(isLeapYear041 ? "是閏年" : "不是閏年");

//ch4 02
let month042 = prompt("請輸入一個月份:");
let days042;
switch (parseInt(month042)) {
    case 1: case 3: case 5: case 7: case 8: case 10: case 12:
        days042 = 31;
        break;
    case 4: case 6: case 9: case 11:
        days042 = 30;
        break;
    case 2:
        days042 = "請考慮閏年的狀況";
        break;
    default:
        days042 = "無效的月份";
}
console.log(days042);

//ch4 03
let str043 = prompt("請輸入一個字符串:");
let reversedStr043 = "";
for (let i043 = str043.length - 1; i043 >= 0; i043--) {
    reversedStr043 += str043[i043];
}
console.log(reversedStr043);

//ch4 04
let rows044 = 5;
for (let i044 = rows044; i044 > 0; i044--) {
    console.log("*".repeat(i044));
}

//ch4 05
let num045 = prompt("請輸入一個數字:");
let isPrime045 = true;
let i045 = 2;
while (i045 <= Math.sqrt(num045)) {
    if (num045 % i045 === 0) {
        isPrime045 = false;
        break;
    }
    i045++;
}
console.log(isPrime045 && num045 > 1 ? "是質數" : "不是質數");

//ch4 06
let rows046 = 5;
let i046 = rows046;
while (i046 > 0) {
    console.log("*".repeat(i046));
    i046--;
}

//ch4 07
let n047 = prompt("請輸入一個正整數:");
let factorial047 = 1;
let i047 = 1;
do {
    factorial047 *= i047;
    i047++;
} while (i047 <= n047);
console.log(factorial047);


//ch4 08
let array048 = [1, 5, 2, 7, 3];
let max048 = array048[0];
for (let num048 of array048) {
    if (num048 > max048) {
        max048 = num048;
    }
}
console.log(max048);

//ch4 09
let array049 = [1, 2, 3, 4, 5, 6, 7, 8];
let sum049 = 0;
for (let num049 of array049) {
    if (num049 % 2 === 0) {
        sum049 += num049;
    }
}
console.log(sum049);

//ch4 10
let obj0410 = {a: 1, b: 2, c: 3, d: 4, e: 5};
let sum0410 = 0;
for (let key0410 in obj0410) {
    sum0410 += obj0410[key0410];
}
console.log(sum0410);