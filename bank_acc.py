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
        self.passbook = [{"cr": self.name, "dr": "-", "amt": self.balance, "timestamp": datetime.now(), "remark": f"Account '{self.name}' created with Balance: Rs. {self.balance:.2f}"}]

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

    # -----Added passbook_entry parameter here, to negate the need to update a already appended entry(that was bad design)----
    def deposit(self, amount, passbook_entry=None):
        self.validate_amount(amount)
        self.balance += amount
        if passbook_entry:
            self.passbook.append(passbook_entry)
        else:
            self.passbook.append({"cr": self.name, "dr": "-", "amt": amount, "timestamp": datetime.now(), "remark": "Deposit"})

    def viable_transaction(self, amount):

        if self.balance < amount:
            return False

        return True

    def validate_amount(self, amount):

        if amount <= 0:
            raise False

        return True

    # ----Added passbook_entry parameter here, to negate the need to update a already appended entry(that was bad design)----
    def withdraw(self, amount, passbook_entry=None):

        if self.validate_amount(amount) and self.viable_transaction(amount):
            self.balance -= amount
            if passbook_entry:
                self.passbook.append(passbook_entry)
            else:
                self.passbook.append({"cr": "-", "dr": self.name, "amt": amount, "timestamp": datetime.now(), "remark": "Withdrawal"})
        else:
            raise BalanceException("Insufficient Balance")

        self.validate_amount(amount)
        self.viable_transaction(amount)

        self.balance -= amount
        if passbook_entry:
            self.passbook.append(passbook_entry)
        else:
            self.passbook.append({"cr": "-", "dr": self.name, "amt": amount, "timestamp": datetime.now(), "remark": "Withdrawal"})

    def transfer(self, amount, recipient):
        if not isinstance(recipient, BankAcc):
            raise ValueError("Invalid Recipient Account !")

        # ------These validations are redundant as self.withdraw already has them------

        # self.validate_amount(amount)
        # self.viable_transaction(amount)

        pb_entry = {"cr": recipient.name, "dr": self.name, "amt": amount, "timestamp": datetime.now(), "remark": f"Transfer from '{self.name}' to '{recipient.name}': Rs. {amount:.2f}"}

        self.withdraw(amount, pb_entry)
        recipient.deposit(amount, pb_entry)

        # self.passbook[-1].update()
        # recipient.passbook[-1].update()

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
        self.passbook.append({"cr": "Bank Interest", "dr": "-", "amt": self.balance, "timestamp": datetime.now(), "remark": f"Added Bank Interest Reward of Rs. {amount*self.interest:.2f}"})

    def choose_interest(self):
        while True:
            try:
                rate = float(input("Choose Interest Rate(1-20%) : ")) * 0.01
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

    fee_percentage = 0.05  # = 5%

    def __init__(self, acc_name, amount):
        super().__init__(acc_name, amount)

    # ----Added passbook_entry parameter here, to negate the need of constantly updating an already appended entry(that was bad design)----
    def withdraw(self, amount, passbook_entry=None):
        # super().withdraw(amount + self.fee)
        # self.passbook[-1].update({"dr": f"'{self.name}', Bank Fee", "remark": f"Withdrawal of Rs. {amount} with Bank Fee: Rs. {self.fee:.2f}"})

        fee_amount = amount * SavingsAcc.fee_percentage
        self.viable_transaction(amount=amount + fee_amount)

        if passbook_entry:
            super().withdraw(amount, passbook_entry)
        else:
            super().withdraw(amount)

        super().withdraw(fee_amount, {"cr": "-", "dr": self.name, "amt": fee_amount, "timestamp": datetime.now(), "remark": "Deduction of Bank Fee"})

    def transfer(self, amount, recipient):
        """
        This function's only job is to validate the transaction with 5% fee added cause its saving's acc
        """

        fee_amount = amount * SavingsAcc.fee_percentage

        self.viable_transaction(amount=amount + fee_amount)
        return super().transfer(amount, recipient)
