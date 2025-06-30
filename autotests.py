import unittest

class BankTransferTests(unittest.TestCase):
    def test_low_amount_commission(self):
        expected_commission = 10  # 10% от суммы
        test_amount = 50
        actual_commission = calculate_commission(test_amount)  
        self.assertEqual(expected_commission, actual_commission,
                         f"Комиссия должна быть {expected_commission}%, а получили {actual_commission}%")

    def test_high_amount_balance_check(self):
        user_balance = 10000  
        transfer_amount = 9980
        self.assertTrue(check_balance(user_balance, transfer_amount),  
                        "Должен быть разрешён перевод при достаточном балансе")

def calculate_commission(amount):
    return 0  

def check_balance(balance, amount):
    return False  

if __name__ == "__main__":
    unittest.main()
