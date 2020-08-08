const rot13 = (str) => {
    // Generating 26 english capital letters
    const letters = [...Array(26).keys()].map((e) =>
        String.fromCharCode(e + 65),
    );
    // Converting the string to array to map every character 13 positions
    //  to the left according to letters array
    return str
        .split("")
        .map((e) => {
            if (e.match(/[A-Za-z]/)) {
                return letters[(letters.indexOf(e) + 26 - 13) % 26];
            } else {
                return e;
            }
            // Converting mapped array back to the string
        })
        .join("");
};

console.log(rot13("SERR PBQR PNZC"));

module.exports = rot13;
