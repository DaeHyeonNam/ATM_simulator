import json
from card import card
from bank import bank

class ATM:
    def __init__(self):
        self.card = card.Card()
        self.bank = bank.BankAPI()
        self.authorization_token = ""
        self.selected_account = ""

    def read_card(self):
        # Get card information
        card_number = input("Please type your card number: ")
        expiration_month = input("Please type your card expiration month: ")
        expiration_year = input("Please type your card expiration year: ")
        cvc = input("Please type your card cvc number: ")

        self.card.set_card_number(card_number)
        self.card.set_expiration_month(expiration_month)
        self.card.set_expiration_year(expiration_year)
        self.card.set_cvc(cvc)


        # Check if the card is valid
        card_information = self.card.get_card_info()
        try:
            response = self.bank.check_card_validity(card_information)
            response = json.loads(response)
        except:
            print("Bank API is not working.")
            exit()

        if(response['success']):
            print("Your card is successfully read.")
        else:
            raise Exception(response['error'])



    def authorize_card(self):
        pin = input("Please type your card PIN number: ")

        if(len(pin) != 4):
            raise Exception("The length of PIN code should be 4.")
        if(not pin.isnumeric()):
            raise Exception("PIN code should be number.")

        card_information = self.card.get_card_info()
        try:
            response = self.bank.get_card_authorization(card_information, int(pin))
            response = json.loads(response)
        except:
            print("Bank API is not working")
            exit()

        if(response['success']):
            self.authorization_token = response['data']['authorization_token']
            print("The card is authorized.")
        else:
            raise Exception(response['error'])

    def select_account(self):
        account_list = self._get_account_list()

        for i, account in enumerate(account_list):
            print(str(i+1) + ". " + account)
        
        account_index_str = input("Please select account: ")
        if(not account_index_str.isnumeric()):
            raise Exception("Please type number.")

        account_index = int(account_index_str)
        if(account_index > len(account_list) + 1 or account_index<=0):
            raise Exception("The account does not exist.")

        self.selected_account = account_list[account_index - 1]

    def execute_task(self):
        task_option_list = ["See balance", "Deposit", "Withdraw", "Quit"]
        select_number = 0

        while(True):
            for i, task_option in enumerate(task_option_list):
                print(str(i+1) + ". " + task_option)
            
            task_index_str = input("Please select task: ")
            if(not task_index_str.isnumeric()):
                raise Exception("Please type number.")

            task_index = int(task_index_str)
            if(task_index >len(task_option_list) + 1 or task_index <= 0):
                raise Exception("The task does not exist.")
            
            if(task_index == 1):
                self.show_balance()
            elif(task_index == 2):
                self.deposit()
            elif(task_index == 3):
                self.withdraw()
            elif(task_index == 4):
                exit()

    def show_balance(self):
        card_information = self.card.get_card_info()

        try:
            response = self.bank.get_account_balance(card_information, self.authorization_token, self.selected_account)
            response = json.loads(response)
        except:
            print("Bank API is not working")
            exit()

        if(response['success']):
            print("Balance: " + str(response['data']['balance']))
        else:
            raise Exception(response['error'])
        
        return response['data']['balance']

    def deposit(self):
        deposit_amount_str = input("How much do you want to deposit? : ")
        assert deposit_amount_str.isnumeric(), "Please type number."

        deposit_amount = int(deposit_amount_str)
        assert deposit_amount >= 0, "The deposit value cannot be negative."

        card_information = self.card.get_card_info()

        try:
            response = self.bank.deposit_into_account(card_information, self.authorization_token, self.selected_account, deposit_amount)
            response = json.loads(response)
        except:
            print("Bank API is not working")
            exit()

        if(response['success']):
            print("Deposit completed successfully.")
            print("Balance: " + str(response['data']['balance']))
        else:
            raise Exception(response['error'])

        return response['data']['balance']

    def withdraw(self):
        withdraw_amount_str = input("How much do you want to withraw? : ")
        assert withdraw_amount_str.isnumeric(), "Please type number."

        withdraw_amount = int(withdraw_amount_str)
        assert withdraw_amount >= 0, "The withdraw value cannot be negative."

        card_information = self.card.get_card_info()

        try:
            response = self.bank.withdraw_from_account(card_information, self.authorization_token, self.selected_account, withdraw_amount)
            response = json.loads(response)
        except:
            print("Bank API is not working")
            exit()

        if(response['success']):
            print("Withdraw completed successfully.")
            print("Balance: " + str(response['data']['balance']))
        else:
            raise Exception(response['error'])
        
        return response['data']['balance']

    def _get_account_list(self):
        card_information = self.card.get_card_info()
        try:
            response = self.bank.get_account_list(card_information, self.authorization_token)
            response = json.loads(response)
        except:
            print("Bank API is not working")
            exit()

        if(response['success']):
            return response['data']['account_list']
        else:
            raise Exception(response['error'])
