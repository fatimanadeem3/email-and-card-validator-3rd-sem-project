import pandas as pd
import numpy as np


def email_checker(email):
    email_rules = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return pd.Series([email]).str.match(email_rules).iloc[0]


def card_checker(card_num):
    stripped_card_num = card_num.replace(" ", "")
    if not pd.Series([stripped_card_num]).str.isnumeric().iloc[0]:
        return False
    digits = np.array(list(map(int, stripped_card_num[::-1])))
    digits[1::2] *= 2
    digits[digits > 9] -= 9
    return digits.sum() % 10 == 0


def read_csv(file_name):
    try:
        return pd.read_csv(file_name).values.tolist()
    except FileNotFoundError:
        return []


def write_csv(file_name, data):
    df = pd.DataFrame(data, columns=["Name", "Detail", "Type", "Status"])
    df.to_csv(file_name, index=False)


def add_entry_to_csv(file_name, name, details, status):
    data = read_csv(file_name)
    data.append([name] + details + [status])
    write_csv(file_name, data)


def bubble_sort_by_name(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][0].lower() > data[j + 1][0].lower():  # Compare names (column 0)
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def display_option():
    print("\n ********* Welcome to Valuation Management System ************")
    print("1. To Check Email Details")
    print("2. To Check Card Valuation Details")
    print("3. To Display CSV Data (Sorted by Name)")
    print("4. To Exit")
    option = input("Enter your choice (1/2/3/4): ")
    return option


def display_csv_data_sorted(file_name):
    data = read_csv(file_name)
    if data:
        sorted_data = bubble_sort_by_name(data)
        print(f"\n Data in {file_name} (Sorted by Name):")
        for record in sorted_data:
            print(", ".join(map(str, record)))
    else:
        print(f"\n No data found in {file_name}.")

def valuation_system():
    validation_file = "validation_records.csv"

    while True:
        option = display_option()

        if option == '1':
            name = input("Enter your name: ")
            email = input("Enter Email Address: ")
            if email_checker(email):
                print(f"The email '{email}' ***** is valid ******.")
                add_entry_to_csv(validation_file, name, [email, "Email"], "Valid")
            else:
                print(f"The email '{email}' ****** is invalid *******. Storing for review.")
                add_entry_to_csv(validation_file, name, [email, "Email"], "Invalid")

        elif option == '2':
            name = input("Enter your name: ")
            card_num = input("Enter card valuation details: ")
            if card_checker(card_num):
                print(f"The card number '{card_num}'******* is valid *******.")
                add_entry_to_csv(validation_file, name, [card_num, "Card"], "Valid")
            else:
                print(f"The card number '{card_num}'******* is invalid ******. Storing for review.")
                add_entry_to_csv(validation_file, name, [card_num, "Card"], "Invalid")

        elif option == '3':
            display_csv_data_sorted(validation_file)

        elif option == '4':
            print("Thank You")
            break

        else:
            print("Invalid option. Please try again.")


valuation_system()
