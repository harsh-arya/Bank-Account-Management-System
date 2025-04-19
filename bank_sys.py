from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc, BalanceException
import sys


class BankMenu:
    
    # Universal Function which takes Title & Options (Dictionary) menu with title, options as attributes
    @staticmethod
    def display(title, options):
        print("\n" + "="*50)
        print(f'{title.upper()}'.center(50))
        print("="*50)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option.title()}")
        print("="*50 + "\n")
        return int(input("Enter your choice : "))


'''
***** SKIP THIS REDUNDAND CODE ******

# Dictionary for Main Menu
# Contains Title and Options for menu function
main_menu={
    "title":"BANKING SYSTEM MENU",
    "option":[
        "Create New Account",
        "Deposit Money",
        "Withdraw Money",
        "Transfer Money",
        "Check Balance",
        "View Transaction History",
        "View All Accounts",
        "View Transaction Log File",
        "Exit"
        ]
}

# Dictionary for Create New Account Menu
create_new_acc_menu={
    "title":"Create New Account",
    "option":[
        "Regular Account",
        "Interest Reward Account",
        "Savings Account",
        "To Main Menu",
        ]
}
'''


class BankSys:

    def __init__(self):
        self.initialize_sys()

    def initialize_sys(self):
        if BankAcc.load_all_acc():
            print(f"Accounts Loaded ...\n{len(BankAcc.all_acc)} Accounts Detected .")
        else :
            print("No Accounts Detected !\nStarting Fresh System :-")

    def run(self):

        while True:

            try:
                choice = BankMenu().display(
                    "BANKING SYSTEM MENU",
                    [
                        "Create New Account",
                        "Deposit Money",
                        "Withdraw Money",
                        "Transfer Money",
                        "Check Balance",
                        "View Transaction History",
                        "View All Accounts",
                        "View Transaction Log File",
                        "Exit"
                    ]
                )

                if choice == 1: self.create_new_acc()
                elif choice == 2: self.deposit_money()
                elif choice == 3: self.withdraw_money()
                elif choice == 4: self.transfer_money()
                elif choice == 5: self.check_balance()
                elif choice == 6: self.view_transac_history()
                elif choice == 7: self.view_all_acc()
                elif choice == 8: self.view_transac_log()
                elif choice == 9: 
                    self.exit_msg()
                    break

                else :
                    print("Invalid Choice !")
            except Exception as e:
                print(f"Error : {str(e)}")

            input("\n\nPlease Enter to continue ...")

    def create_new_acc(self):
        choice = BankMenu().display(
            "Create New Account",
            [
                "Regular Account",
                "Interest Reward Account",
                "Savings Account",
                "To Main Menu",
            ]
        )

        if choice <= 1 and choice >= 3 :
            print("Invalid Choice !")
            return

        # Taking details and validating them
        acc_name= input("Enter Account Name : ")
        acc = BankAcc.find_acc(acc_name)
        if acc :
            print("Account already exists !")
            return
        balance = float(input("Enter Balance : "))
        if balance <= 0:
            print("Invalid \nBalance must be positive value !")
            return

        # Creating Account(class object)
        if choice == 1: acc = BankAcc(acc_name, balance)
        elif choice == 2: acc = InterestRewardAcc(acc_name, balance)
        elif choice == 3: acc = SavingsAcc(acc_name, balance)

        print(f"Account '{acc_name}' created successfully.")

    def deposit_money(self):
        print("Deposit Money :".center(50,'*'))
        acc_name= input("Enter Account Name : ")
        acc = BankAcc.find_acc(acc_name)
        if not acc:
            print("Account doesn't exist !")
            return
        amount = float(input("Enter Amount : "))
        if amount <= 0:
            print("Invalid \nAmount must be positive value !")
            return
        acc.deposit(amount)
        
    def withdraw_money(self):
        print("Withdrawing Money :".center(50,'*'))
        acc_name= input("Enter Account Name : ")
        acc = BankAcc.find_acc(acc_name)
        if not acc :
            print("Account doesn't exist !")
            return
        amount = float(input("Enter Amount to withdraw : "))
        if amount <= 0 and amount > acc.balance :
            print("Invalid \nAmount must be positive value !")
            return
        acc.withdraw(amount)

    def transfer_money(self):
        print("Transferring Money :".center(50,'*'))
        sender_name = input("Enter Sender's Account Name : ").strip()
        recipient_name = input("Enter Receiver's Account Name : ").strip()
        
        sender = BankAcc.find_acc(sender_name)
        if not sender:
            print(f"Sender account '{sender_name}' doesn't exist!")
            return
        
        recipient = BankAcc.find_acc(recipient_name)
        if not recipient:
            print(f"Recipient account '{recipient_name}' doesn't exist!")
            return
        
        try:
            amount = float(input("Enter Transfer Amount : "))
            if amount <= 0:
                print("Invalid amount! Amount must be positive.")
                return
            
            sender.transfer(amount, recipient)
            print(f"Successfully transferred Rs.{amount:.2f} from '{sender.name}' to '{recipient.name}'")
        except ValueError:
            print("Invalid amount! Please enter a valid number.")
        except BalanceException as e:
            print(f"Transfer failed: {str(e)}")
        except Exception as e:
            print(f"An error occurred during transfer: {str(e)}")

        def check_balance(self):
            print("Checking Account Balance :".center(50,'*'))
            acc_name= input("Enter Account Name : ")
            acc = BankAcc.find_acc(acc_name)
            if not acc :
                print("Account doesn't exist !")
                return
            acc.show_balance()

    def view_transac_history(self):
        acc_name= input("Enter Account Name : ")
        acc = BankAcc.find_acc(acc_name)
        if not acc :
            print("Account doesn't exist !")
            return
        print("\n" + "Checking Transaction History :".center(50,'*') + "\n")
        for txn in acc.transaction_history:
            print(f"-> {txn}")


    def view_all_acc(self):
        if not BankAcc.all_acc:
            print("No Existing Accounts yet !")
            return

        print("\n" + "="*50)
        print(("All Accounts List").upper().center(50)+ "\n\n")
        print(f"{'Name' :<20} {'Acc-Type' :<20} {'Balance' :<10}")
        print("="*50)
        for acc in BankAcc.all_acc:
            acc_type = "Regular"
            if isinstance(acc, InterestRewardAcc):
                acc_type = "Interest Reward"
            if isinstance(acc, SavingsAcc):
                acc_type = "Savings"
            print(f"{acc.name:<20} {acc_type:<20} Rs.{acc.balance:<10}")
        print("="*50 + "\n")

    def view_transac_log(self):
        try:
            with open(BankAcc.transaction_log_file, "r") as file:
                print("\n" + "="*50)
                print(("Transaction Log").upper().center(50))
                print("="*50)
                print(file.read())
                print("="*50 + "\n")
        except Exception as e:
            print(f"Error in Loading File : {str(e)}")

    def exit_msg(self):
        # Save before exiting
        BankAcc.save_all_acc()
        print("Thank you for using the Banking System!")