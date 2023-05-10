# Author: Jomar Malpica
# Course: CS 361
# Date: 2023-05-08


import time
import json
import zmq
from datetime import datetime


def checkIndustryIdentifier(cc_info):
    """
    Checks the credit card number and compares it to the "Major Industry "Identifier"" number 
    to verify it is valid.
    Return: tuple
    """

    industry_identifier = {
        "Visa":{"identifier":[4], "digits":16}, 
        "Discover":{"identifier":[6], "digits":16},
        "Mastercard":{"identifier":[5,2], "digits":16},
        "AmericanExpress":{"identifier":[3], "digits":15},
    }

    cc_info = json.loads(cc_info)
    cc_first_digit = int((cc_info['ccnumber'])[0])
    cc_digit_num = len(cc_info["ccnumber"]) - cc_info["ccnumber"].count(" ")

    if cc_first_digit not in industry_identifier[cc_info["ccissuer"]]["identifier"]:
        return ("Invalid Idenfifier Number.")

    if cc_digit_num != industry_identifier[cc_info["ccissuer"]]["digits"]:
        return ("Invalid Number of Digits.")

    return ("Valid.")


def checkExpirationDate(cc_info):
    """
    Checks that the credit card expiration date is valid.
    Returns: tuple
    """
    
    cc_info = json.loads(cc_info)
    current_month = datetime.now().month
    current_year = datetime.now().year
    cc_expdate = (int(cc_info["expdate"][0:2]), int("20" + cc_info["expdate"][3:5]))

    if cc_expdate[1] > current_year and (cc_expdate[1] - current_year) < 7:
        return ("Valid.")

    if cc_expdate[1] == current_year and cc_expdate[0] < current_month:
        return ("Valid.")

    return ("Invalid Expiration Date.")


def creditCardValidator(cc_info):
    """
    Takes credit card information and checks if its valid or not. 
    Returns: boolean
    """

    validation = checkIndustryIdentifier(cc_info)

    if validation != "Valid.":
        return validation

    return checkExpirationDate(cc_info)
    
    
def main():

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        cc_info = socket.recv()
        print("Received request...")

        #  Send reply back to client
        socket.send_string(creditCardValidator(cc_info))


if __name__ == "__main__":
    main()