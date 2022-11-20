from utils import utils

class BankAPI:
    '''
    Temporal bank API mimicking the real bank API
    '''
    def __init__(self):
        self.small_db = {
            '1234567812345678': {
                'pin' : 1234, 
                "account_list": {
                    "Account1": {
                        "balance" : 1000
                    }, 
                    "Account2": {
                        "balance" : 1000
                    }, 
                    "Account3": {
                        "balance" : 1000
                    }
                }
            }
        }

    def check_card_validity(self, card_information):
        return self._is_card_valid(card_information)

    def get_card_authorization(self, card_information, pin_input):
        if(self._get_pin_code(card_information) == pin_input):
            return utils.Utility.make_success_response({'authorization_token': self._get_authorization_token()})
        else:
            return utils.Utility.make_failure_response("PIN code is not correct.")

    def get_account_list(self, card_information, authorization_token):
        if(self._is_token_valid(card_information, authorization_token)):
            account_list = list(self.small_db[card_information[0]]['account_list'].keys())
            return utils.Utility.make_success_response({'account_list': account_list})
        else:
            return utils.Utility.make_failure_response('Card information or authorization code is not correct.')

    def get_account_balance(self, card_information, authorization_token, account):
        if(self._is_token_valid(card_information, authorization_token)):
            return utils.Utility.make_success_response({'balance': self.small_db[card_information[0]]['account_list'][account]['balance']})
        else:
            return utils.Utility.make_failure_response('Card information or authorization code is not correct.')

    def deposit_into_account(self, card_information, authorization_token, account, amount):
        if(self._is_token_valid(card_information, authorization_token)):
            self.small_db[card_information[0]]['account_list'][account]['balance'] += amount
            return utils.Utility.make_success_response({'balance': self.small_db[card_information[0]]['account_list'][account]['balance']})
        else:
            return utils.Utility.make_failure_response('Card information or authorization code is not correct.')
            

    def withdraw_from_account(self, card_information, authorization_token, account, amount):
        if(self._is_token_valid(card_information, authorization_token)):
            isBalanceEnough = self.small_db[card_information[0]]['account_list'][account]['balance'] > amount

            if(isBalanceEnough):
                self.small_db[card_information[0]]['account_list'][account]['balance'] -= amount
                return utils.Utility.make_success_response({'balance': self.small_db[card_information[0]]['account_list'][account]['balance']})
            
            else:
                return utils.Utility.make_failure_response('Balance is not enough.')
        else:
            return utils.Utility.make_failure_response('Card information or authorization code is not correct.')
            


    # private methods
    def _is_card_valid(self, card_information):
        card_number, expiration_month, expiration_year, cvc = card_information
        if(card_number == "1234567812345678"):
            return utils.Utility.make_success_response({})
        else:
            return utils.Utility.make_failure_response("The card is not valid.") 

    def _get_pin_code(self, card_information):
        card_number, expiration_month, expiration_year, cvc = card_information
        return self.small_db[card_number]['pin']

    def _get_authorization_token(self):
        return 'ABCD'

    def _is_token_valid(self, card_information, authorization_token):
        card_number, expiration_month, expiration_year, cvc = card_information

        if(card_number == "1234567812345678" and authorization_token == self._get_authorization_token()):
            return True
        else:
            return False