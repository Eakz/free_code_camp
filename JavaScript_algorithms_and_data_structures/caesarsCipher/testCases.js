const rot13 = require("./caesarsCipher");

const data = [
    ["SERR PBQR PNZC", "FREE CODE CAMP"],
    ["SERR CVMMN!", "FREE PIZZA!"],
    ["SERR YBIR?", "FREE LOVE?"],
    [
        "GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT.",
        "QUICK BROWN FOX JUMPS OVER THE LAZY DOG.",
    ],
];
let passedTests = 0;
let amountFailed = 0;
data.forEach(([e, a]) => {
    console.log("INPUT - ", e);
    console.log("Result ", rot13(e));
    console.log("Comparison, - required result <<< ", a, " >>>");
    console.log("-".repeat(e.length));
    if (rot13(e) === a) {
        console.log("<<<< PASSED >>>>\n");
        passedTests++;
    } else {
        console.log("<<<< FAILED >>>>\n");
        amountFailed++;
    }
});
console.log("\n", "*".repeat(passedTests), "-".repeat(amountFailed));
