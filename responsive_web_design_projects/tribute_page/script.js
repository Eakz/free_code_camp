const data = [
    "<li><strong>1914</strong> - Born in Cresco, Iowa</li>",
    "<li>\n<strong>1933</strong> - Leaves his family's farm to attend the\nUniversity of Minnesota, thanks to a Depression era program known as the\n\"National Youth Administration\"\n</li>",
    "<li>\n<strong>1935</strong> - Has to stop school and save up more money. Works\nin the Civilian Conservation Corps, helping starving Americans. \"I saw\nhow food changed them\", he said. \"All of this left scars on me.\"\n</li>",
    "<li>\n<strong>1937</strong> - Finishes university and takes a job in the US\nForestry Service\n</li>",
    "<li>\n<strong>1938</strong> - Marries wife of 69 years Margret Gibson. Gets\nlaid off due to budget cuts. Inspired by Elvin Charles Stakman, he\nreturns to school study under Stakman, who teaches him about breeding\npest-resistent plants.\n</li>",
    "<li>\n<strong>1941</strong> - Tries to enroll in the military after the Pearl\nHarbor attack, but is rejected. Instead, the military asked his lab to\nwork on waterproof glue, DDT to control malaria, disinfectants, and\nother applied science.\n</li>",
    "<li>\n<strong>1942</strong> - Receives a Ph.D. in Genetics and Plant Pathology\n</li>",
    "<li>\n<strong>1944</strong> - Rejects a 100% salary increase from Dupont,\nleaves behind his pregnant wife, and flies to Mexico to head a new plant\npathology program. Over the next 16 years, his team breeds 6,000\ndifferent strains of disease resistent wheat - including different\nvarieties for each major climate on Earth.\n</li>",
    "<li>\n<strong>1945</strong> - Discovers a way to grown wheat twice each\nseason, doubling wheat yields\n</li>",
    "<li>\n<strong>1953</strong> - crosses a short, sturdy dwarf breed of wheat\nwith a high-yeidling American breed, creating a strain that responds\nwell to fertilizer. It goes on to provide 95% of Mexico's wheat.\n</li>",
    "<li>\n<strong>1962</strong> - Visits Delhi and brings his high-yielding\nstrains of wheat to the Indian subcontinent in time to help mitigate\nmass starvation due to a rapidly expanding population\n</li>",
    "<li><strong>1970</strong> - receives the Nobel Peace Prize</li>",
    "<li>\n<strong>1983</strong> - helps seven African countries dramatically\nincrease their maize and sorghum yields\n</li>",
    "<li>\n<strong>1984</strong> - becomes a distinguished professor at Texas A&amp;M\nUniversity\n</li>",
    "<li>\n<strong>2005</strong> - states \"we will have to double the world food\nsupply by 2050.\" Argues that genetically modified crops are the only way\nwe can meet the demand, as we run out of arable land. Says that GM crops\nare not inherently dangerous because \"we've been genetically modifying\nplants and animals for a long time. Long before we called it science,\npeople were selecting the best breeds.\"\n</li>",
    "<li><strong>2009</strong> - dies at the age of 95.</li>"
]
const ul = document.querySelector('ul')
console.log(ul)
data.forEach(e=>{
    ul.innerHTML+=e
});
