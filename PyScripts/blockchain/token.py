class Token:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balance = {}

    def mint(self, account, amount):
        if account in self.balance:
            self.balance[account] += amount
        else:
            self.balance[account] = amount

    def transfer(self, sender, receiver, amount):
        if sender in self.balance and self.balance[sender] >= amount:
            self.balance[sender] -= amount
            if receiver in self.balance:
                self.balance[receiver] += amount
            else:
                self.balance[receiver] = amount
            return True
        return False

# Usage example:
my_token = Token("MyToken", "MTK", 1000000)
my_token.mint("Address1", 500)
my_token.transfer("Address1", "Address2", 200)
