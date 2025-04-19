import pickle
from datetime import datetime
from os import path


class BalanceException(Exception):
    pass


class BankAcc:

    # List of BankAcc objects
    all_acc = []
    # transaction_log_file = "transaction_log.txt"
    data_file = "acc_info.dat"

    def __init__(self, acc_name, amount):
        self.name = acc_name
        self.balance = amount
        self.acc_num = self.generate_acc_num()
        self.transaction_history= []
        self.passbook = [
            {"cr": self, "db": None, "amt": self.balance, "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")  }
            ]

        # msg = f"Account '{self.name}' created with Balance of Rs.{self.balance:.2f}"
        # self.log(msg)

        # Adding new object(account) into class list all_acc
        # self.__class__.all_acc.append(self)
        BankAcc.append_acc_list(self)

    @classmethod
    def append_acc_list(cls, obj):
        cls.all_acc.append(obj)

    def generate_acc_num(self):
        return hash(f"({self.name}{datetime.now().timestamp()})") % 1000000

    def show_balance(self):
        return (f"Account '{self.name}'\nBalance = Rs.{self.balance:.2f}")
        # self.log("Checked Balance.")

    def deposit(self, amount):
        self.validate_amount(amount)
        self.balance += amount
        # msg=f"Deposit of Amount: Rs.{amount} completed."
        # print(msg)
        # self.log(msg)

    def viable_transaction(self, amount):
        if self.balance <= amount:
            raise BalanceException(
                f"Sorry, '{self.name}' only has a balance of Rs.{self.balance:.2f}."
            )
        
    def validate_amount(self, amount):
        if amount <= 0:
            raise ValueError(f"Amount must be positive.")

    def withdraw(self, amount):
        self.validate_amount(amount)
        self.viable_transaction(amount)
        self.balance -= amount
        # msg = f"Withdrawl of Amount: Rs.{amount} completed."
        # self.log(msg)

    def transfer(self, amount, recipient):
        if not isinstance(recipient, BankAcc):
            raise ValueError("Invalid Recipient Account !")
        
        self.validate_amount(amount)
        self.viable_transaction(amount)

        self.balance -= amount
        recipient.balance += amount

        # sen_msg = f"Transferred Rs.{amount} to Recipient'{recipient.name}'."
        # rec_msg = f"Received  Rs.{amount} from Sender'{self.name}' transferred."
        # self.log(sen_msg)
        # recipient.log(rec_msg)

    # # Log transaction and account activities in object private list
    # def log(self, message):
    #     timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #     log_entry = f"{timestamp} - {message}"
    #     self.transaction_history.append(log_entry)
    #     print(log_entry)
    #     self.log_to_file(log_entry)

    # # Log transaction and account activities in transaction log file
    # def log_to_file(self, log_entry):
    #     with open(self.transaction_log_file, "a") as f:
    #         f.write("-> " + log_entry + "\n")

    # # Log transaction and account activities in transaction log file
    # @classmethod
    # def cls_log_to_file(cls, message):
    #     timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #     with open(cls.transaction_log_file, "a") as f:
    #         f.write(f"{timestamp} - {message}\n")

    # Find Object( Account ) from Account Name
    @classmethod
    def find_acc(cls, acc_name):
        if not acc_name or not isinstance(acc_name, str):
            return None
        # for acc in cls.all_acc:
        #     if acc.name.strip().lower() == acc_name.strip().lower():
        #         return acc
        
        # Generator Function
        if acc_name in ( acc.name for acc in cls.all_acc):
            return acc
        return None

    # Save Transaction History of each object (account) to the given file
    @classmethod
    def save_all_acc(cls):
        try:
            # with automatically closes file
            with open(cls.data_file, "wb") as file:
                pickle.dump(cls.all_acc, file)
            # cls.cls_log_to_file(message= "SYSTEM - All Accounts Saved .")
            return True
        except Exception as e:
            print(f"Error Saving Accounts : {type(e).__name__}")
            return False

    # Load all accounts to system
    @classmethod
    def load_all_acc(cls):
        try:
            if not path.exists(cls.data_file):
                with open(cls.data_file, "rb") as file:
                    cls.all_acc = pickle.load(file)
                # cls.cls_log_to_file(message= "SYSTEM - All Accounts Loaded .")
                return True
            return False
        except Exception as e:
            print(f"Error Loading Accounts : {type(e).__name__}")
            return False


class InterestRewardAcc(BankAcc):
    def __init__(self, acc_name, amount):
        super().__init__(acc_name, amount)
        interest = self.choose_interest()
        self.balance += amount * interest
        # msg = (f"Interest Rewarded = {interest}%")
        # self.log(msg)

    def choose_interest(self):
        while True:
            try:
                rate = float(input("Choose interst rate(%) : "))*.01
                if 0 < rate <= 0.2 :
                    return rate                  
                else: 
                    print("Invalid input!")   
            except Exception as error:
                print(f"Invalid input! {type(error).__name__}\n")
                print(f"Type : {type(error).__name__}\n")
                print(f"Message : {str(error)}")

    
class SavingsAcc(BankAcc):
    def __init__(self, acc_name, amount):
        super().__init__(acc_name, amount)
        self.fee=5
        # msg = (f"Fee Structure: Rs.{self.fee} charged per withdrawl")
        # self.log(msg)

    def withdraw(self, amount):
        try:
            self.viable_transaction(amount + self.fee)
            self.validate_amount(amount + self.fee)
            self.balance -= (amount + self.fee)
            # msg = f"Withdrawl of Amount: Rs.{amount} completed."
            # self.log(msg)

        except BalanceException as error:
            msg = f"\nWithdrawl interrupted . {error}"
            # self.log(msg)
