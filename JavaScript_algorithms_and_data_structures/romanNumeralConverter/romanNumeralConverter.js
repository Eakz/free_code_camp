const convertToRoman = (num) => {
    const romans = {
        1000: "M",
        500: "D",
        100: "C",
        50: "L",
        10: "X",
        5: "V",
        1: "I",
    };
    const combas = {
        900: "CM",
        400: "CD",
        90: "XC",
        40: "XL",
        9: "IX",
        4: "IV",
    };
    // Combining keys in one array with reversed allignment(from higher to lower)
    const keys = [Object.keys(romans).reverse(), Object.keys(combas).reverse()];
    // Initializing the answer
    let answer = "";
    // Iterating through each key in combas and romans to fish out valid letters
    for (let i = 0; i < Object.keys(romans).length; i++) {
        // Defining fst to see if the amount left holds any key[] amount
        let fst = Math.floor(num / keys[0][i]);
        if (fst > 0) {
            answer += romans[keys[0][i]].repeat(fst);
            num = num - fst * keys[0][i];
        }
        // Checking for combinations in the ...rest
        if (keys[1][i]) {
            let fst = Math.floor(num / keys[1][i]);
            if (fst > 0) {
                answer += combas[keys[1][i]];
                num = num - keys[1][i];
            }
        }
    }
    // Returning the answer
    return answer;
};


module.exports = convertToRoman;
