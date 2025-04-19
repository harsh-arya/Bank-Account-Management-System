# BANK ACCOUNT MANAGEMENT SYSTEM

#from bank_acc import BankAcc, InterestRewardAcc, SavingsAcc
from bank_sys import BankSys
#from os import path
import sys

if __name__=="__main__":
    try:
        BankSys().run()
    except:
        print("\nSystem shutdown requested")
        sys.exit(0)


