class Category:
    # Initializing class
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0
    # Using __str__ instead of __repr__ for explicit wordy console representation
    def __str__(self):
        def amount(i): return f"{float(i['amount']):.2f}"
        return f"{self.name.center(30,'*')}\n" + "\n".join([f"{i['description'][:23]}{(30-len(amount(i))-len(i['description'][:23]))*' '}{amount(i)}" for i in self.ledger])+f"\nTotal: {self.balance:.2f}"
    
    def get_balance(self):
        return self.balance

    def check_funds(self, amount):
        return amount <= self.balance

    def deposit(self, amount, description=""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if(self.check_funds(amount)):
            self.deposit(-amount, description)
            return True
        return False

    def transfer(self, amount, other):
        transaction = self.withdraw(amount, f"Transfer to {other.name}")
        if(transaction):
            other.deposit(amount, f"Transfer from {self.name}")
            return True
        return False


def create_spend_chart(categories):
    percentages = [i for i in range(0, 110, 10)]
    perCategory = [sum([j["amount"]*-1 for j in i.ledger if j['amount']<0]) for i in categories]
    perCategory = [i/sum(perCategory)*100 for i in perCategory]
    perc=perCategory
    os = [reversed([f'o '  if perc[i]>=j else '  ' for j in percentages]) for i in range(len(categories))]
    percentages = [f"{i}|".rjust(4,' ') for i in percentages]
    max_length = max([len(i.name) for i in categories])
    categories_names = [i.name.ljust(max_length,' ') for i in categories]
    return "Percentage spent by category\n"+'\n'.join([''.join([f"{j} " for j in i]) for i in zip(reversed(percentages),*os)])+f'\n{4*" "}{(len(categories)*3+1)*"-"}\n'+'\n'.join([f"{' '*5}{''.join([f'{j}  ' for j in i])}" for i in zip(*[list(j) for j in categories_names])])

# test = Category('Vagina-Torments')
# test2 = Category('Alonas-Anal')
# test.deposit(15, 'for love and lessons and all the rabbits')
# test.deposit(1000, 'Just do it')
# test.withdraw(1500, 'hehyey')
# test.transfer(30, test2)
# test.transfer(300000, test2)
# test2.deposit(300,'sdf')
# test2.withdraw(30,'asdgfrwg')
# test.withdraw(300,'asfdgfskjksnlnk')
# print(test)
# print(test2)
# print(create_spend_chart([test, test2]))
# food = Category("Food")
# entertainment= Category('Entertainment')
# food.deposit(900, "deposit")
# food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
# food.transfer(20, entertainment)
# actual = str(food)
# expected = f"*************Food*************\ndeposit                 900.00\nmilk, cereal, eggs, bac -45.67\nTransfer to Entertainme -20.00\nTotal: 834.33"

# print(actual,expected,sep="\n\n\n")
# food = Category("Food")
# entertainment = Category("Entertainment")
# business= Category("Business")
# food.deposit(900, "deposit")
# entertainment.deposit(900, "deposit")
# business.deposit(900, "deposit")
# food.withdraw(105.55)
# entertainment.withdraw(33.40)
# business.withdraw(10.99)
# actual = create_spend_chart([business, food, entertainment])
# expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "
# print(actual, expected,sep="\n\n\n")
# print(business,food,entertainment)
# print(actual)