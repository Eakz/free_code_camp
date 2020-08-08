const palindrome = (str)=>{
    // Refining the str to array filtering out any non-alpha/non-digit characters
    const refined = str.toLowerCase().split('').filter(e=>e.match(/[A-Za-z0-9]/));
    // Returning the boolean expression of equality of original string vs reversed variant
    return refined.join('')===refined.reverse().join('')
}

module.exports = palindrome;
  
  
  