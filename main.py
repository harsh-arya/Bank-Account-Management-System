# BANK ACCOUNT MANAGEMENT SYSTEM

from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc, BalanceException
from my_module import refactor, menu
from os import system
import sys


global current_user
current_user = None


def login():
    global current_user

    while True:
        try:
            acc_name = input("Enter Account Name : ")
            acc = BankAcc.find_acc(refactor(acc_name))
            if acc:
                current_user = acc
                break
        except Exception as error:
            print(f"Login Error: {str(error)}")


def confirm_login(acc):
    global current_user

    choice = input(refactor(f"Do you want to login with '{acc.name}'(y/n): "))
    if choice == 'y':
        current_user = acc
        print("Log in successful !")
        return
    elif choice == 'n':
        print("Login-Initiation Terminated!")
    else:
        print("Invalid choice!")


def logout():
    global current_user
    
    if current_user:
        print(f"Account '{current_user.name}' logged out ...")
    else:
        print("No Account Logged In!")
    current_user = None


# To Validate Account for:-
#   True:   Check whether acc exists before acc-creation
#   False:  Check whether acc doesn't exist for transactions
def validate_acc(acc_name, validity=False):
    acc = BankAcc.find_acc(refactor(acc_name))

    # For True Validity, validate for Account-Creation
    if validity:
        if acc:
            print(f"Account '{acc_name}' already exists!")
        return None

    if not acc:
        print(f"Account '{acc_name}' doesn't exist!")
        return None
    return acc


def validate_balance(amount, limit=None):
    try:
        if amount <= 0:
            print("Invalid amount! Amount must be positive.")
            return
        if limit is not None:
            if amount > limit:
                print("Invalid amount!\nAmount cannot exceed {limit:.2f} !")
                return
        
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
    except BalanceException as e:
        print(f"Transfer failed: {str(e)}")


def initialize_system():
    system("clear")
    if BankAcc.load_all_acc():
        print(f"Accounts Loaded ...\n{len(BankAcc.all_acc)} Accounts Detected .")
    else:
        print("No Accounts Detected !\nStarting Fresh System :-")


def create_new_acc():
    choice = menu(
        [
            "Create New Account",
        ],
        [
            "Regular Account",
            "Interest Reward Account",
            "Savings Account",
            "To Main Menu",
        ]
    )
    if not choice:
        return

    try:
        # Taking details and validating them
        acc_name = input("Enter Account Name : ")
        acc = validate_acc(acc_name, True)
        balance = float(input("Enter Balance : "))
        validate_balance(balance)
    except Exception as error:
        print(f"Error: {str(error)}")

    # Creating Account(class object)
    if choice == 1: acc = BankAcc(acc_name, balance)
    elif choice == 2: acc = InterestRewardAcc(acc_name, balance)
    elif choice == 3: acc = SavingsAcc(acc_name, balance)

    print(f"Account '{acc_name}' created successfully.")

    confirm_login(acc)


def deposit_money():
    print("Deposit Money :".center(50, '*'))

    # Taking details and validating them
    if not current_user:
        acc_name = input("Enter Account Name : ")
        acc = validate_acc(acc_name)
        confirm_login(acc)

    else:
        acc = current_user

    amount = float(input("Enter Amount : "))
    validate_balance(amount)
    
    acc.deposit(amount)
    print(f"Successful Deposit: Rs. {amount:.2f}")
    

def withdraw_money():
    print("Withdrawing Money :".center(50, '*'))

    # Taking details and validating them
    if not current_user:
        acc_name = input("Enter Account Name : ")

        acc = validate_acc(acc_name)
        confirm_login(acc)

    else:
        acc = current_user
        
    amount = float(input("Enter Amount to withdraw : "))
    validate_balance(amount, acc.balance)
    
    acc.withdraw(amount)
    print(f"Successful Withdrawal: Rs. {amount:.2f}")


def transfer_money():
    print("Transferring Money :".center(50, '*'))

    # Taking details and validating them
    if not current_user:
        sender_name = input("Enter Sender's Account Name : ")
        sender = validate_acc(sender_name)
        confirm_login(sender)
    
    else:
        sender = current_user
        
    recipient_name = input("Enter Receiver's Account Name : ")
    
    recipient = BankAcc.find_acc(refactor(recipient_name))
    if not recipient:
        print(f"Recipient account '{recipient_name}' doesn't exist!")
        return
    
    try:
        amount = float(input("Enter Transfer Amount : "))
        validate_balance(amount)

        sender.transfer(amount, recipient)
        print(f"Successful Transfer : '{sender.name}' : Rs.{amount:.2f} -> '{recipient.name}'")

    except Exception as e:
        print(f"Transfer failed: {str(e)}")


def check_balance():
    print("Checking Account Balance :".center(50, '*'))

    # Taking details and validating them
    if not current_user:
        acc_name = input("Enter Account Name : ")
        acc = validate_acc(acc_name)
        confirm_login(acc)
        
    else:
        acc = current_user
    print(acc.show_balance())


def view_transac_history():
    print("\n" + "Checking Transaction History :".center(50, '*') + "\n")

    # Taking details and validating them
    if not current_user:
        acc_name = input("Enter Account Name : ")
        acc = validate_acc(acc_name)
        confirm_login(acc)

    else:
        acc = current_user
        
    print("\n" + '='*130)
    print("Transaction Table :".center(130) + "\n")
    print("\n" + '='*130)
    print(
        f"{'S.No.':<8}"
        f"{'Date & Time':<22}"
        f"{'Credit':<20}"
        f"{'Debit':<20}"
        f"{'Balance':<10}"
        f"{'Remark':<30}"
    )
    print("\n" + '='*130)

    for i, txn in enumerate(acc.passbook, 1):
        print(
            f"{i:<8}"
            f"{txn['timestamp'].strftime('%d-%m-%Y %H:%M:%S'):<22}"
            f"{txn['cr']:<20}"
            f"{txn['dr']:<20}"
            f"{txn['amt']:<10}"
            f"{txn['remark']:<30}"
        )
    
    print("\n" + '='*130)


def view_all_acc():
    if not BankAcc.all_acc:
        print("No Existing Accounts yet !")
        return
    print(f"{len(BankAcc.all_acc)} Accounts are detected.")

    print("\n" + "="*70)
    print(("All Accounts List").upper().center(70) + "\n")
    print("\n" + "="*70)
    print(f"{'S.no.':<8}{'Name' :<25}{'Acc-Type' :<22}{'Balance' :<15}")
    print("="*70)

    # Finding Object Type (Account Type)
    for i, acc in enumerate(BankAcc.all_acc, 1):
        acc_type = "Regular"
        if isinstance(acc, InterestRewardAcc):
            acc_type = "Interest Reward"
        if isinstance(acc, SavingsAcc):
            acc_type = "Savings"
        
        print(f"{i:<8}{acc.name:<25} {acc_type:<22} Rs.{acc.balance:<15}")
    print("="*70 + "\n")


def exit_msg():
    # Save before exiting
    BankAcc.save_all_acc()
    print("Thank you for using the Banking System!")
    sys.exit()


initialize_system()

while True:
    
    current_user_status = "Guest Login"
    if current_user:
        current_user_status = f"Logged In:'{current_user.name}'"
    
    try:
        choice = menu(
            [
                "BANKING SYSTEM MENU",
                f"{current_user_status}"
            ],
            [
                "Create New Account",
                "Deposit Money",
                "Withdraw Money",
                "Transfer Money",
                "Check Balance",
                "View Transaction History",
                "View All Accounts",
                "Logout",
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
        elif choice == 8: logout()
        elif choice == 9: 
            exit_msg()
            break
        else:
            print("Invalid Choice !")
    
    except Exception as e:
        print(f"{type(e).__name__} : {str(e)}")
        SystemExit(0)

    input("\n\nPlease Enter to continue ...")
    system("clear")

