import random

def Generate_pass(length = 12):
    upper_case_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_case_letters = upper_case_letters.lower()
    numbers = "1234567890"
    special_characters = "`~!@#$%^&*()-_=+,./;'[]\<>?:|"

    character_list = upper_case_letters + lower_case_letters + numbers + special_characters

    pasword = ''

    for i in range(length):
        pasword += random.choice(character_list)

    return pasword