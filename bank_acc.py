# Bank Account Core Logic Class

import pickle
from datetime import datetime
from os import path


class BalanceException(Exception):
    pass


class BankAcc:

    # List of BankAcc objects
    all_acc = []
    data_file = "acc_info.dat"

    def __init__(self, acc_name, amount):
        self.name = acc_name
        self.balance = amount
        self.acc_num = self.generate_acc_num()
        # List of dictionary comprising Creditor, Debitor, Amount along with Timestamp
        self.passbook = [
            {
                "cr": f"'{self.name}'",
                "dr": "-",
                "amt": self.balance,
                "timestamp": datetime.now(),
                "remark": f"Account '{self.name}' created with Balance: Rs. {self.balance:.2f}",
            }
        ]

        # Adding new object(account) into class list all_acc
        # self.__class__.all_acc.append(self)
        BankAcc.append_acc_list(self)

    @classmethod
    def append_acc_list(cls, obj):
        cls.all_acc.append(obj)

    def generate_acc_num(self):
        return hash(f"({self.name}{datetime.now().timestamp()})") % 1000000

    def show_balance(self):
        return f"Account '{self.name}'\nBalance = Rs.{self.balance:.2f}"

    def deposit(self, amount, passbook_entry=None):
        self.validate_amount(amount)
        self.balance += amount

        if passbook_entry:
            self.passbook.append(passbook_entry)
        else:
            self.passbook.append(
                {
                    "cr": f"'{self.name}'",
                    "dr": "-",
                    "amt": amount,
                    "timestamp": datetime.now(),
                    "remark": f"Deposit of Amount: Rs. {amount:.2f}",
                }
            )

    def viable_transaction(self, amount):
        if self.balance < amount:
            raise BalanceException(
                f"Sorry, '{self.name}' only has a balance of Rs.{self.balance:.2f}."
            )

    def validate_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")

    def withdraw(self, amount, passbook_entry=None):
        # Validating amount and transaction
        self.validate_amount(amount)
        self.viable_transaction(amount)

        self.balance -= amount

        if passbook_entry:
            self.passbook.append(passbook_entry)
        else:
            self.passbook.append(
                {
                    "cr": "-",
                    "dr": f"'{self.name}'",
                    "amt": amount,
                    "timestamp": datetime.now(),
                    "remark": f"Withdrawal of Amount: Rs. {amount:.2f}",
                }
            )

    def transfer(self, amount, recipient):
        if not isinstance(recipient, BankAcc):
            raise ValueError("Invalid Recipient Account !")

        passbook_entry = {
            "cr": f"'{recipient.name}'",
            "dr": f"'{self.name}'",
            "amt": amount,
            "timestamp": datetime.now(),
            "remark": f"Transfer from '{self.name}' to '{recipient.name}': Rs. {amount:.2f}",
        }

        self.withdraw(amount, passbook_entry)
        recipient.deposit(amount, passbook_entry)

    # Find Object( Account ) from Account Name
    @classmethod
    def find_acc(cls, acc_name):
        if not acc_name or not isinstance(acc_name, str):
            return None

        # # Generator Function
        # if acc_name in ( acc.name.strip().title() for acc in cls.all_acc):
        # # It can't Return acc.
        #     print("Found .")

        for acc in cls.all_acc:
            if acc.name.strip().lower() == acc_name:
                return acc
        return None

    # Save Transaction History of each object (account) to the given file
    @classmethod
    def save_all_acc(cls):
        try:
            # with automatically closes file
            with open(cls.data_file, "wb") as file:
                pickle.dump(cls.all_acc, file)
            return True
        except Exception as e:
            print(f"Error Saving Accounts : {type(e).__name__} : {str(e)}")
            return False

    # Load all accounts to system
    @classmethod
    def load_all_acc(cls):
        try:
            if path.exists(cls.data_file):
                with open(cls.data_file, "rb") as file:
                    cls.all_acc = pickle.load(file)
                if cls.all_acc:
                    return True
            return False
        except Exception as e:
            print(f"Error Loading Accounts : {type(e).__name__} : {str(e)}")
            return False


class InterestRewardAcc(BankAcc):
    def __init__(self, acc_name, amount):
        super().__init__(acc_name, amount)
        self.interest = self.choose_interest()
        self.balance += amount * self.interest
        self.passbook.append(
            {
                "cr": "Bank Interest",
                "dr": "-",
                "amt": self.balance,
                "timestamp": datetime.now(),
                "remark": f"Added Bank Interest Reward of Rs. {amount*self.interest:.2f}",
            }
        )

    def choose_interest(self):
        while True:
            try:
                rate = float(input("Choose Interst Rate(1-20%) : ")) * 0.01
                if 0 < rate <= 0.2:
                    return rate
                print("Invalid input! Interest Rate must be within (1-20%).")
            except ValueError:
                print("Invalid input! Please enter Numerical Value.")
            except Exception as error:
                print("Invalid input!\n")
                print(f"Type : {type(error).__name__}\n")
                print(f"Message : {str(error)}")


class SavingsAcc(BankAcc):
    def __init__(self, acc_name, amount):
        super().__init__(acc_name, amount)
        self.fee = 5.00

    def withdraw(self, amount, passbook_entry=None):
        if passbook_entry is None:
            passbook_entry = {
                "cr": "-",
                "dr": f"'{self.name}', Bank Fee",
                "amt": amount,
                "timestamp": datetime.now(),
                "remark": f"Withdrawal of Rs. {amount:.2f} with Bank Fee: Rs. {self.fee:.2f}",
            }
        super().withdraw(amount + self.fee, passbook_entry)


"""
# Checking Logic & Functionality
if __name__ == "__main__":
    try:
        new = SavingsAcc(acc_name="new", amount=500)
        new_two = SavingsAcc(acc_name="new_two", amount=500)

        print(new.show_balance())
        print(new_two.show_balance())

        new.withdraw(500)
        print(new.show_balance())
        print(new_two.show_balance())

        # new.transfer(494.99, new_two)
        # print(new.show_balance())
        # print(new_two.show_balance())

        # for i, txn in enumerate(new.passbook, 1):
        #     print(
        #         f"{i:<8}{txn['timestamp'].strftime('%d-%m-%Y %H:%M:%S'):<22}{txn['cr']:<20}{txn['dr']:<20}{txn['amt']:<10}{txn['remark']:<30}"
        #     )
        #     print("\n")
        # for txn in new_two.passbook:
        #     print(txn)
        #     print("\n")

        # list = [{"arg1": "name1", "arg2": 1}]
        # print(list)
        # list = [{"arg1": "name1_m"}]
        # print(list)
        # list.append({"arg1": "name2", "arg2": 2})
        # print(list)
        # list = [{"arg1": "name2_m", "arg2": 2}]
        # print(list)
        # for i, entry in enumerate(list, 1):
        #     print(f"{i}) {entry}")

    except Exception as error:
        print(f"System Shutdown!\nError : {str(error)}")
        SystemExit(0)

    finally:
        print(new.show_balance())
        print(new_two.show_balance())
"""
