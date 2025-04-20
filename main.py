# BANK ACCOUNT MANAGEMENT SYSTEM

from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc, BalanceException
from my_module import refactor, menu
from os import path, system
import sys

def initialize_system():
    system("clear")
    if BankAcc.load_all_acc():
        print(f"Accounts Loaded ...\n{len(BankAcc.all_acc)} Accounts Detected .")
    else :
        print("No Accounts Detected !\nStarting Fresh System :-")

def run():

    while True:

        try:
            choice = menu(
                "BANKING SYSTEM MENU",
                [
                    "Create New Account",
                    "Deposit Money",
                    "Withdraw Money",
                    "Transfer Money",
                    "Check Balance",
                    "View Transaction History",
                    "View All Accounts",
                    "Exit"
                ]
            )

            system("clear")

            if choice == 1: create_new_acc()
            elif choice == 2: deposit_money()
            elif choice == 3: withdraw_money()
            elif choice == 4: transfer_money()
            elif choice == 5: check_balance()
            elif choice == 6: view_transac_history()
            elif choice == 7: view_all_acc()
            elif choice == 8: 
                exit_msg()
                break
            else :
                print("Invalid Choice !")
        
        except Exception as e:
            print(f"{type(e).__name__} : {str(e)}")

        input("\n\nPlease Enter to continue ...")
        system("clear")

def create_new_acc():
    choice = menu(
        "Create New Account",
        [
            "Regular Account",
            "Interest Reward Account",
            "Savings Account",
            "To Main Menu",
        ]
    )
    if not choice:
        return

    # Taking details and validating them
    acc_name= input("Enter Account Name : ")
    acc = BankAcc.find_acc(refactor(acc_name))
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

def deposit_money():
    print("Deposit Money :".center(50,'*'))

    # Taking details and validating them
    acc_name= input("Enter Account Name : ")

    acc = BankAcc.find_acc(refactor(acc_name))
    if not acc:
        print("Account doesn't exist !")
        return
    amount = float(input("Enter Amount : "))
    if amount <= 0:
        print("Invalid \nAmount must be positive value !")
        return
    
    acc.deposit(amount)
    
def withdraw_money():
    print("Withdrawing Money :".center(50,'*'))

    # Taking details and validating them
    acc_name= input("Enter Account Name : ")

    acc = BankAcc.find_acc(refactor(acc_name))
    if not acc :
        print("Account doesn't exist !")
        return
    amount = float(input("Enter Amount to withdraw : "))
    if amount <= 0 and amount > acc.balance :
        print("Invalid \nAmount must be positive value !")
        return
    
    acc.withdraw(amount)

def transfer_money():
    print("Transferring Money :".center(50,'*'))

    # Taking details and validating them
    sender_name = input("Enter Sender's Account Name : ")
    recipient_name = input("Enter Receiver's Account Name : ")
    
    sender = BankAcc.find_acc(refactor(sender_name))
    if not sender:
        print(f"Sender account '{sender_name}' doesn't exist!")
        return
    
    recipient = BankAcc.find_acc(refactor(recipient_name))
    if not recipient:
        print(f"Recipient account '{recipient_name}' doesn't exist!")
        return
    
    try:
        amount = float(input("Enter Transfer Amount : "))
        if amount <= 0:
            print("Invalid amount! Amount must be positive.")
            return
        
        sender.transfer(amount, recipient)
        print(f"Successfully Transfer : '{sender.name}' : Rs.{amount:.2f} -> '{recipient.name}'")
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
    except BalanceException as e:
        print(f"Transfer failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred during transfer: {str(e)}")

def check_balance():
    print("Checking Account Balance :".center(50,'*'))

    # Taking details and validating them
    acc_name= input("Enter Account Name : ")

    acc = BankAcc.find_acc(refactor(acc_name))
    if not acc :
        print("Account doesn't exist !")
        return
    
    print(acc.show_balance())

def view_transac_history():
    print("\n" + "Checking Transaction History :".center(50,'*') + "\n")

    # Taking details and validating them
    acc_name= input("Enter Account Name : ")
    acc = BankAcc.find_acc(refactor(acc_name))
    if not acc :
        print("Account doesn't exist !")
        return
    
    print("\n" + '='*130)
    print("Transaction Table :".center(130) + "\n")
    print(f"{'S.No.':<8}{'Date & Time':<22}{'Creditor':<20}{'Debitor':<20}{'Balance':<10}{'Remark':<30}")

    for i,txn in enumerate(acc.passbook, 1):
        print(f"{i:<8}{txn['timestamp']:<22}{txn['cr']:<20}{txn['dr']:<20}{txn['amt']:<10}{txn['remark']:<30}")
    
    print("\n" + '='*130)

def view_all_acc():
    if not BankAcc.all_acc:
        print("No Existing Accounts yet !")
        return

    print("\n" + "="*50)
    print(("All Accounts List").upper().center(50)+ "\n\n")
    print(f"{'Name' :<20} {'Acc-Type' :<20} {'Balance' :<10}")
    print("="*50)

    # Finding Object Type (Account Type)
    for acc in BankAcc.all_acc:
        acc_type = "Regular"
        if isinstance(acc, InterestRewardAcc):
            acc_type = "Interest Reward"
        if isinstance(acc, SavingsAcc):
            acc_type = "Savings"
        
        print(f"{acc.name:<20} {acc_type:<20} Rs.{acc.balance:<10}")
    print("="*50 + "\n")

def exit_msg():
    # Save before exiting
    BankAcc.save_all_acc()
    print("Thank you for using the Banking System!")
    sys.exit()


if __name__=="__main__":
    try:
        initialize_system()
        run()
    except:
        print("\nSystem shutdown requested")
        sys.exit(0)


