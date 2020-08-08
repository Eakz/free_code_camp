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
    const keys = [Object.keys(romans).reverse(), Object.keys(combas).reverse()];
    let answer = "";
    for (let i = 0; i < Object.keys(romans).length; i++) {
        let fst = Math.floor(num / keys[0][i]);
        if (fst > 0) {
            answer += romans[keys[0][i]].repeat(fst);
            num = num - fst * keys[0][i];
        }
        if (keys[1][i]) {
            let fst = Math.floor(num / keys[1][i]);
            if (fst > 0) {
                answer += combas[keys[1][i]];
                num = num - keys[1][i];
            }
        }
    }

    return answer;
};


module.exports = convertToRoman;
