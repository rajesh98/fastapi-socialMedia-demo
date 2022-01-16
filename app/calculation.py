def add(n1:int, n2:int):
    return n1+n2


class BankAccount():
    def __init__(self, start_balance = 0):
        self.balaance = start_balance
    
    def deposit(self,amount):
        self.balaance += amount

    def withdraw(self,amount):
        self.balaance -= amount

    def collect_interest(self):
        self.balaance *= 1.1
