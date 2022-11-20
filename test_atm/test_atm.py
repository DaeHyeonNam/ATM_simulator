from unittest import TestCase
from unittest.mock import patch
from atm import atm

class TestATM(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestATM, self).__init__(*args, **kwargs)
        self.atm = atm.ATM()

    def test_read_card(self):
        # failure cases
        failure_input_list = [
            # month error
            [
                '1234567812345678',
                '32',
                '23',
                '123'
            ], 
            # year error
            [
                '1234567812345678',
                '01',
                '43',
                '123'
            ], 
            # card number length error
            [
                '00000000',
                '12',
                '23',
                '123'
            ],
            # cvc length error
            [
                '1234567812345678',
                '12',
                '23',
                '44'
            ],
            # not existing card number
            [
                '1111111111111111',
                '12',
                '23',
                '123'
            ]
        ]
        for failure_input in failure_input_list:
            with patch('builtins.input', side_effect=failure_input):
                self.assertRaises(Exception, lambda: self.atm.read_card())

        # success case
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()

    def test_authorize_card(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()

        # test 
        # failure cases
        failure_input_list = [
            # PIN length is not 4
            [
                '12'
            ],
            # PIN code is not number
            [
                'hihi'
            ],
            # wrong pin
            [
                '4321'
            ],
        ]
        for failure_input in failure_input_list:
            with patch('builtins.input', side_effect=failure_input):
                self.assertRaises(Exception, lambda: self.atm.authorize_card())

        # success caes
        success_input = [
            '1234'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.authorize_card()

    def test_select_account(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123',
            '1234'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()
            self.atm.authorize_card()

        # failure input
        failure_input_list = [
            [
                'a'
            ],
            [
                '0'
            ]
        ]
        for failure_input in failure_input_list:
            with patch('builtins.input', side_effect=failure_input):
                self.assertRaises(Exception, lambda: self.atm.select_account())

        # success input
        success_input = [
            '3'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.select_account()

    def test_execute_task(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123',
            '1234',
            '3'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()
            self.atm.authorize_card()
            self.atm.select_account()

        # failure input
        failure_input_list = [
            [
                'a'
            ],
            [
                '5'
            ]
        ]
        for failure_input in failure_input_list:
            with patch('builtins.input', side_effect=failure_input):
                self.assertRaises(Exception, lambda: self.atm.execute_task())
        
        # success input
        success_input = [
            '1',
            '4'
        ]
        with patch('builtins.input', side_effect=success_input):
            with self.assertRaises(SystemExit):
                    self.atm.execute_task()

    
    def test_show_balance(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123',
            '1234',
            '3'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()
            self.atm.authorize_card()
            self.atm.select_account()
        
        # balance function test
        balance = self.atm.show_balance()
        self.assertEqual(balance, 1000)
        
    
    
    def test_deposit(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123',
            '1234',
            '1'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()
            self.atm.authorize_card()
            self.atm.select_account()
        
        # balance function test
        deposit_input = [
            '2333'
        ]
        with patch('builtins.input', side_effect=deposit_input):
            balance = self.atm.deposit()
            self.assertEqual(balance, 3333)

        
    def test_withdraw(self):
        # previous state
        success_input = [
            '1234567812345678',
            '05',
            '23',
            '123',
            '1234',
            '2'
        ]
        with patch('builtins.input', side_effect=success_input):
            self.atm.read_card()
            self.atm.authorize_card()
            self.atm.select_account()
        
        # balance function test
        withdraw_failure_input = [
            '40000'
        ]
        with patch('builtins.input', side_effect=withdraw_failure_input):
            self.assertRaises(Exception, lambda: self.atm.withdraw())
            
        withdraw_success_input = [
            '800'
        ]
        with patch('builtins.input', side_effect=withdraw_success_input):
            balance = self.atm.withdraw()
            self.assertEqual(balance, 200)

