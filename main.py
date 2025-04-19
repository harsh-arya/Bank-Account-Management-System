# BANK ACCOUNT MANAGEMENT SYSTEM

#from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc
from bank_sys import BankSys
#from os import path
import sys

# if not path.exists ("acc_info.txt"):
#     f = open("acc_info.txt", 'x')

    # harsh = BankAcc("Harsh Arya", 1000)
    # flick = BankAcc("Flick Arya", 5000)

    # harsh.show_balance()
    # harsh.deposit(500)
    # harsh.withdraw(5000)
    # #harsh.viable_transaction(10000)

    # harsh.transfer(500, flick)

    # kick = InterestRewardAcc("Kick Arya", 2000)

    # vick = SavingsAcc(acc_name="Vick Arya", amount=3000)
    # vick.withdraw(1000)

    # new = BankAcc(acc_name="new", amount=5000)

    # BankAcc.save_all_acc(file_name="acc_info.txt")


if __name__=="__main__":
    try:
        BankSys().run()
    except:
        print("\nSystem shutdown requested")
        sys.exit(0)


