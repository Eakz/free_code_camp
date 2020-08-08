const telephoneCheck = (str) => {
    // matching to telephone REGEX with brackets on 1st trio of digits
    const matchy = str.match(/^1?\s?\d{3}\s?\-?\d{3}\-?\s?\d{4}/);
    // matching to telephone REGEX without brackets on 1st trio of digits ( I totally retardingly lazy to write conditionals)
    const matchy2 = str.match(/^1?\s?\({1}\d{3}\){1}\s?\-?\d{3}\-?\s?\d{4}/);
    // if either of the matches works then evaluate the input with the matched part
    if (matchy) {
        return matchy.input === matchy[0];
    } else if (matchy2) {
        return matchy2.input === matchy2[0];
    } else {
        return false;
    }
};
console.log(telephoneCheck("(6054756961)"));
console.log(telephoneCheck("(555)555-5555"));
console.log(telephoneCheck("6054756961"));
console.log(telephoneCheck("555-5555"));
module.exports = telephoneCheck;
