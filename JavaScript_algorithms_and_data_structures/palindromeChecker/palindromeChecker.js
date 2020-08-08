const palindrome = (str)=>{
    const refined = str.toLowerCase().split('').filter(e=>e.match(/[A-Za-z0-9]/));
    console.log(refined)
    return refined.join('')===refined.reverse().join('')
}

module.exports = palindrome;
  
  
  