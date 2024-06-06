//ch6 0101
function daysFromToday0601(date0601) {
    let today0601 = new Date();
    let inputDate0601 = new Date(date0601);
    let timeDifference0601 = today0601 - inputDate0601;
    let daysDifference0601 = Math.floor(timeDifference0601 / (1000 * 60 * 60 * 24));
    return daysDifference0601;
}

// 示例調用:
console.log(daysFromToday0601("2024-01-01"));  // 根據當前日期輸出天數差

//ch6 0102
function reverseString0602(str0602) {
    return str0602.split("").reverse().join("");
}

// 示例調用:
console.log(reverseString0602("hello"));  // 輸出: "olleh"

//ch6 0103
function isPalindrome0603(str0603) {
    let cleanedStr0603 = str0603.replace(/[^a-zA-Z0-9]/g, "").toLowerCase();
    let reversedStr0603 = cleanedStr0603.split("").reverse().join("");
    return cleanedStr0603 === reversedStr0603;
}

// 示例調用:
console.log(isPalindrome0603("A man, a plan, a canal, Panama"));  // 輸出: true


//ch6 0201
function generateRandomString0601(length0601) {
    let characters0601 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result0601 = "";
    for (let i0601 = 0; i0601 < length0601; i0601++) {
        let randomIndex0601 = Math.floor(Math.random() * characters0601.length);
        result0601 += characters0601[randomIndex0601];
    }
    return result0601;
}

// 示例調用:
console.log(generateRandomString0601(10));  // 輸出：隨機生成10個字符長的字符串

//ch6 0202
function isPerfectNumber0602(num0602) {
    let sum0602 = 0;
    for (let i0602 = 1; i0602 <= num0602 / 2; i0602++) {
        if (num0602 % i0602 === 0) {
            sum0602 += i0602;
        }
    }
    return sum0602 === num0602;
}

// 示例調用:
console.log(isPerfectNumber0602(28));  // 輸出: true

//ch6 0203
function bubbleSort0603(arr0603) {
    let n0603 = arr0603.length;
    for (let i0603 = 0; i0603 < n0603 - 1; i0603++) {
        for (let j0603 = 0; j0603 < n0603 - 1 - i0603; j0603++) {
            if (arr0603[j0603] > arr0603[j0603 + 1]) {
                let temp0603 = arr0603[j0603];
                arr0603[j0603] = arr0603[j0603 + 1];
                arr0603[j0603 + 1] = temp0603;
            }
        }
    }
    return arr0603;
}

// 示例調用:
console.log(bubbleSort0603([5, 2, 9, 1, 5, 6]));  // 輸出: [1, 2, 5, 5, 6, 9]
