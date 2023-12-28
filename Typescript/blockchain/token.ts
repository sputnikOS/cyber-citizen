class Token {
    public name: string;
    public symbol: string;
    public totalSupply: number;
    public balance: { [key: string]: number };

    constructor(name: string, symbol: string, totalSupply: number) {
        this.name = name;
        this.symbol = symbol;
        this.totalSupply = totalSupply;
        this.balance = {};
    }

    mint(account: string, amount: number): void {
        if (this.balance[account]) {
            this.balance[account] += amount;
        } else {
            this.balance[account] = amount;
        }
    }

    transfer(sender: string, receiver: string, amount: number): boolean {
        if (this.balance[sender] && this.balance[sender] >= amount) {
            this.balance[sender] -= amount;
            this.balance[receiver] = this.balance[receiver] ? this.balance[receiver] + amount : amount;
            return true;
        }
        return false;
    }
}

// Usage example:
const myToken = new Token("MyToken", "MTK", 1000000);
myToken.mint("Address1", 500);
myToken.transfer("Address1", "Address2", 200);
