# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from atm import atm

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    atm = atm.ATM()

    # get card information
    atm.read_card()

    # get authorization
    atm.authorize_card()

    # select account 
    atm.select_account()

    # execute task
    atm.execute_task()


