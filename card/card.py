from datetime import date

class Card:
    def __init__(self):
        self.card_number = ""
        self.cvc = 0
        self.expiration_month= 0
        self.expiration_year = 0

    def set_card_number(self, card_number):
        if(len(card_number) != 16):
            raise Exception( "The length of card number should be 16.")

        self.card_number = card_number

    def set_cvc(self, cvc):
        if(len(cvc) != 3):
            raise Exception("The length of cvc should be 3.")
        if(not cvc.isnumeric()):
            raise Exception("CVC should be a numeric value.")

        self.cvc = int(cvc)

    def set_expiration_month(self, expiration_month):
        if(int(expiration_month) > 12):
            raise Exception("The expiration month is invalid.")

        self.expiration_month = expiration_month

    def set_expiration_year(self, expiration_year):
        card_max_life = 10 # temporal card max life
        card_max_expiration_year = int(date.today().year) - 2000 + card_max_life

        if(int(expiration_year) >= card_max_expiration_year):
            raise Exception("The expiration year is invalid")

        self.expiration_year = expiration_year

    def get_card_info(self):
        return self.card_number, self.expiration_month, self.expiration_year, self.cvc