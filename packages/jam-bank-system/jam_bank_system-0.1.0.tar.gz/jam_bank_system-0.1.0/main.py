#type: ignore
import json
import os
from typing import Dict, Optional

class BankAccount:
    """Class representing a bank account"""
    def __init__(self, username: str, password: str, balance: float = 0.0):
        self.username = username
        self.password = password
        self.balance = balance
        self.transactions = []

    def deposit(self, amount: float) -> bool:
        """Deposit money into account"""
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount:.2f}")
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account"""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount:.2f}")
            return True
        return False

    def get_balance(self) -> float:
        """Get current balance"""
        return self.balance

    def get_transaction_history(self) -> list:
        """Get transaction history"""
        return self.transactions

class Bank:
    """Class managing all bank accounts"""
    def __init__(self, db_file: str = "bank_data.json"):
        self.db_file = db_file
        self.accounts: Dict[str, BankAccount] = self._load_accounts()

    def _load_accounts(self) -> Dict[str, BankAccount]:
        """Load accounts from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                return {username: BankAccount(username, info['password'], info['balance'])
                       for username, info in data.items()}
        return {}

    def _save_accounts(self):
        """Save accounts to JSON file"""
        data = {username: {'password': account.password, 'balance': account.balance}
                for username, account in self.accounts.items()}
        with open(self.db_file, 'w') as f:
            json.dump(data, f)

    def create_account(self, username: str, password: str) -> bool:
        """Create a new bank account"""
        if username in self.accounts:
            return False
        self.accounts[username] = BankAccount(username, password)
        self._save_accounts()
        return True

    def login(self, username: str, password: str) -> Optional[BankAccount]:
        """Login to existing account"""
        if username in self.accounts and self.accounts[username].password == password:
            return self.accounts[username]
        return None

def main():
    """Main CLI interface"""
    bank = Bank()
    
    while True:
        print("\n=== Bank Management System ===")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            account = bank.login(username, password)
            
            if account:
                print(f"Welcome, {username}!")
                while True:
                    print("\n=== Account Menu ===")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transaction History")
                    print("5. Logout")
                    
                    option = input("Enter choice (1-5): ")
                    
                    if option == '1':
                        print(f"Balance: ${account.get_balance():.2f}")
                    elif option == '2':
                        try:
                            amount = float(input("Enter amount to deposit: $"))
                            if account.deposit(amount):
                                print("Deposit successful!")
                                bank._save_accounts()
                            else:
                                print("Invalid amount!")
                        except ValueError:
                            print("Invalid input!")
                    elif option == '3':
                        try:
                            amount = float(input("Enter amount to withdraw: $"))
                            if account.withdraw(amount):
                                print("Withdrawal successful!")
                                bank._save_accounts()
                            else:
                                print("Invalid amount or insufficient funds!")
                        except ValueError:
                            print("Invalid input!")
                    elif option == '4':
                        history = account.get_transaction_history()
                        if history:
                            print("\nTransaction History:")
                            for transaction in history:
                                print(transaction)
                        else:
                            print("No transactions yet!")
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("Invalid credentials!")
                
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if bank.create_account(username, password):
                print("Account created successfully!")
            else:
                print("Username already exists!")
                
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()