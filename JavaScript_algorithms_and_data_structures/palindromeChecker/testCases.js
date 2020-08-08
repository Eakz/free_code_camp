const palindrome = require("./palindromeChecker");

const data = [
    ["eye", true],
    ["_eye", true],
    ["race car", true],
    ["not a palindrome", false],
    ["A man, a plan, a canal. Panama", true],
    ["never odd or even", true],
    ["My age is 0, 0 si ega ym.", true],
    ["nope", false],
    ["0_0 (: /- :) 0-0", true],
    ["business", false],
    ['1 eye for of 1 eye.',false]
];
let passedTests = 0;
let amountFailed = 0;
data.forEach(([e, a]) => {
    console.log("INPUT - ", e);
    console.log("Result ", palindrome(e));
    console.log(
        "Comparison, - required result <<< ",
        palindrome(e) === a,
        " >>>",
    );
    console.log("-".repeat(e.length));
    if (palindrome(e) === a) {
        console.log("<<<< PASSED >>>>\n");
        passedTests++;
    } else {
        console.log("<<<< FAILED >>>>\n");
        amountFailed++;
    }
});
console.log("\n", "*".repeat(passedTests), "-".repeat(amountFailed));
