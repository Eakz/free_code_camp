const rot13 = (str) => {
    const letters = [...Array(26).keys()].map((e) =>
        String.fromCharCode(e + 65),
    );
    return str.split("").map((e) => {
        if (e.match(/[A-Za-z]/)) {
            return letters[(letters.indexOf(e) + 26 - 13) % 26];
        } else {
            return e;
        }
    }).join('');
};

console.log(rot13("SERR PBQR PNZC"));

module.exports = rot13;
