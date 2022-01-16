# This file is just for practicing some testing features available im pytest
#this file does not contain any testcases or code responsible for the main application



import pytest
from app.calculation import add, BankAccount


@pytest.fixture()
def zero_bank_acc():
    return BankAccount()

@pytest.fixture()
def nonzero_bank_acc():
    return BankAccount(100)
 

@pytest.mark.parametrize("x,y,expected", [
    (2,3,5),
    (9,10,19)
])
def test_add(x,y,expected):
    assert add(x,y) == expected


def test_set_Bank_account(zero_bank_acc):
    assert zero_bank_acc.balaance==0

def test_deposit(nonzero_bank_acc):
    nonzero_bank_acc.deposit(1000) 
    assert nonzero_bank_acc.balaance==1100








        




