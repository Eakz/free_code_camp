const romanNumeral = require("./romanNumeralConverter");

const data = [
    [1, "I"],
    [3, "III"],
    [4, "IV"],
    [5, "V"],
    [9, "IX"],
    [12, "XII"],
    [16, "XVI"],
    [29, "XXIX"],
    [44, "XLIV"],
    [45, "XLV"],
    [68, "LXVIII"],
    [83, "LXXXIII"],
    [97, "XCVII"],
    [99, "XCIX"],
    [400, "CD"],
    [500, "D"],
    [501, "DI"],
    [649, "DCXLIX"],
    [798, "DCCXCVIII"],
    [891, "DCCCXCI"],
    [1000, "M"],
    [1004, "MIV"],
    [1023, "MXXIII"],
    [2014, "MMXIV"],
    [3999, "MMMCMXCIX"],
    [13, "XIII"],
];
let passedTests = 0;
let amountFailed = 0;
data.forEach(([e, a]) => {
    console.log("INPUT - ", e);
    console.log("Result ", romanNumeral(e));
    console.log("Comparison, - required result <<< ", a, " >>>");
    console.log("-".repeat(e.length));
    if (romanNumeral(e) === a) {
        console.log("<<<< PASSED >>>>\n");
        passedTests++;
    } else {
        console.log("<<<< FAILED >>>>\n");
        amountFailed++;
    }
});
console.log("\n", "*".repeat(passedTests), "-".repeat(amountFailed));
