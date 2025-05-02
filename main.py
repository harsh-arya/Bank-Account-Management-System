# BANK ACCOUNT MANAGEMENT SYSTEM

from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc
from my_module import refactor, menu
from os import system
import sys

current_user = None


def login():
    global current_user

    max_attempts = 3
    total_attempts = 0

    while total_attempts < max_attempts:
        try:
            acc_name = refactor(input("Enter Account Name : "))
            acc = BankAcc.find_acc(acc_name)
            if acc:
                current_user = acc
                return
            else:
                raise ValueError("Couldn't find the account")

        except Exception as error:
            print(f"Login Error: {str(error)}\n")
            total_attempts += 1
            print(f"Remaining attempts: {max_attempts-total_attempts}\n")

    print("Exiting....")
    sys.exit()


def logout():
    global current_user

    if current_user:
        print(f"Account '{current_user.name}' logged out ...")
    else:
        print("No Account Logged In!")
    current_user = None


def initialize_system():
    system("clear")
    if BankAcc.load_all_acc():
        print(f"Accounts Loaded ...\n{len(BankAcc.all_acc)} Accounts Detected .")
    else:
        print("No Accounts Detected !\nStarting Fresh System :-")


def create_new_acc():

    global current_user
    choice = menu(
        [
            "Create New Account",
        ],
        [
            "Regular Account",
            "Interest Reward Account",
            "Savings Account",
            "Cancel",
        ],
    )
    if abs(choice) > 3:
        sys.exit()

    try:
        # Taking details and validating them
        acc_name = refactor(input("Enter Account Name : "))
        balance = float(input("Enter Balance : "))

        if balance > 100000000 or balance <= 0:
            raise ValueError("Invalid Initial Balance")

        if choice == 1:
            current_user = BankAcc(acc_name, balance)
        elif choice == 2:
            current_user = InterestRewardAcc(acc_name, balance)
        elif choice == 3:
            current_user = SavingsAcc(acc_name, balance)

    except Exception as error:
        print(f"Error: {str(error)}")
        return

    print(f"Account '{acc_name}' created successfully.")


def deposit_money():
    print("Deposit Money :".center(50, "*"))

    try:
        amount = float(input("Enter Amount : "))
        current_user.deposit(amount)
        print(f"Successful Deposit: Rs. {amount:.2f}")
    except Exception as error:
        print(f"Error: {str(error)}")
        return


def withdraw_money():
    print("Withdrawing Money :".center(50, "*"))

    amount = float(input("Enter Amount to withdraw : "))

    try:
        current_user.withdraw(amount)
        print(f"Successful Withdrawal: Rs. {amount:.2f}")
    except Exception as error:
        print(f"Error: {str(error)}")


def transfer_money():
    print("Transferring Money :".center(50, "*"))
    sender = current_user

    recipient_name = refactor(input("Enter Receiver's Account Name : "))

    recipient = BankAcc.find_acc(refactor(recipient_name))
    if not recipient:
        print(f"Recipient account '{recipient_name}' doesn't exist!")
        return

    try:
        amount = float(input("Enter Transfer Amount : "))

        sender.transfer(amount, recipient)
        print(f"Successful Transfer : '{sender.name}' : Rs.{amount:.2f} -> '{recipient.name}'")

    except Exception as e:
        print(f"Transfer failed: {str(e)}")


def check_balance():
    print("Checking Account Balance :".center(50, "*"))
    print(current_user.show_balance())


def view_transac_history():
    print("\n" + "Checking Transaction History :".center(50, "*") + "\n")
    print("\n" + "=" * 130)
    print("Transaction Table :".center(130) + "\n")
    print("\n" + "=" * 130)
    print(f"{'S.No.':<8}" f"{'Date & Time':<22}" f"{'Credit':<20}" f"{'Debit':<20}" f"{'Balance':<10}" f"{'Remark':<30}")
    print("\n" + "=" * 130)

    for i, txn in enumerate(current_user.passbook, 1):
        print(f"{i:<8}" f"{txn['timestamp'].strftime('%d-%m-%Y %H:%M:%S'):<22}" f"{txn['cr']:<20}" f"{txn['dr']:<20}" f"{txn['amt']:<10}" f"{txn['remark']:<30}")

    print("\n" + "=" * 130)


def view_all_acc():
    if not BankAcc.all_acc:
        print("No Existing Accounts yet !")
        return
    print(f"{len(BankAcc.all_acc)} Accounts are detected.")

    print("\n" + "=" * 70)
    print(("All Accounts List").upper().center(70) + "\n")
    print("\n" + "=" * 70)
    print(f"{'S.no.':<8}{'Name':<25}{'Acc-Type':<22}{'Balance':<15}")
    print("=" * 70)

    # Finding Object Type (Account Type)
    for i, acc in enumerate(BankAcc.all_acc, 1):
        acc_type = "Regular"
        if isinstance(acc, InterestRewardAcc):
            acc_type = "Interest Reward"
        if isinstance(acc, SavingsAcc):
            acc_type = "Savings"

        print(f"{i:<8}{acc.name:<25} {acc_type:<22} Rs.{acc.balance:<15}")
    print("=" * 70 + "\n")


def main_menu():

    while True:
        choice = menu(["Choose An Option"], ["Login", "Sign Up", "Exit"])

        try:
            if choice == 1:
                login()
                break
            elif choice == 2:
                create_new_acc()
                break
            else:
                sys.exit()
        except Exception as e:
            print(e)
            sys.exit()


# --------Execution Starts Here----------


initialize_system()
main_menu()

while True:

    choice = menu(
        ["BANKING SYSTEM MENU", f"{current_user.name}"],
        ["Deposit Money", "Withdraw Money", "Transfer Money", "Check Balance", "View Transaction History", "View All Accounts", "Logout", "Exit"],
    )

    try:
        if choice == 1:
            deposit_money()
        elif choice == 2:
            withdraw_money()
        elif choice == 3:
            transfer_money()
        elif choice == 4:
            check_balance()
        elif choice == 5:
            view_transac_history()
        elif choice == 6:
            view_all_acc()
        elif choice == 7:
            logout()
            main_menu()
        elif choice == 8:
            print("Thank you for using the Banking System!")
            sys.exit()
        else:
            print("Invalid Choice !")

    except Exception as e:
        print(e)
    finally:
        BankAcc.save_all_acc()

    input("\n\nPlease Enter to continue ...")
