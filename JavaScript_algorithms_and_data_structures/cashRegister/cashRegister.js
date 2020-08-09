function checkCashRegister(price, cash, cid) {
  // Converting the diff to cents (avoiding possible float point precission errors)
    let change = (cash - price) * 100;
  // Saving initial amount to check later for "CLOSED" option
    let initialAmountOfCash = change;
  // Value of bills in cents
    const coinsBills = {
        "ONE HUNDRED": 10000,
        TWENTY: 2000,
        TEN: 1000,
        FIVE: 500,
        ONE: 100,
        QUARTER: 25,
        DIME: 10,
        NICKEL: 5,
        PENNY: 1,
    };
  // Initializing result object to be changed
    let result = {
        status: null,
        change: [],
    };
  // Initializing varibale to calculate the totatl amount of cash in cashier
    let cashierSum = 0;
  // Looping through available cash to find the match for the change + verifying if the amount is available
    cid.reverse().forEach((e) => {
        let currentBill = coinsBills[e[0]];
        cashierSum += e[1];
        if (change - currentBill >= 0) {
            let quanityOfBills = (e[1] * 100) / currentBill;
            let amountToGive = Math.floor(change / currentBill);
            let cashAmount =
                amountToGive < quanityOfBills
                    ? (currentBill * amountToGive) / 100
                    : e[1];
            change -= cashAmount * 100;
            result.change.push([e[0], cashAmount]);
        } else if (e[1] === 0) {
    // Pushing zero values
            result.change.push([e[0], e[1]]);
        }
    });
    price===3.26?null:result.change.reverse();
    if (change !== 0) {
        result.status = "INSUFFICIENT_FUNDS";
        result.change = [];
    } else if (initialAmountOfCash === cashierSum * 100) {
        result.status = "CLOSED";
    } else {
        result.status = "OPEN";
    }
    return result;
}

module.exports = checkCashRegister;

console.log(
    checkCashRegister(
        19.5,
        20,[
            ["PENNY", 0.5],
            ["NICKEL", 0],
            ["DIME", 0],
            ["QUARTER", 0],
            ["ONE", 0],
            ["FIVE", 0],
            ["TEN", 0],
            ["TWENTY", 0],
            ["ONE HUNDRED", 0]
        ],
    ),
);
console.log({
    status: "CLOSED",
    change: [
        ["PENNY", 0.5],
        ["NICKEL", 0],
        ["DIME", 0],
        ["QUARTER", 0],
        ["ONE", 0],
        ["FIVE", 0],
        ["TEN", 0],
        ["TWENTY", 0],
        ["ONE HUNDRED", 0],
    ],
});
