from source.model.database_manager import change_public_and_private_key_status, store_public_key, get_public_and_private_key_status, get_public_key, get_balance, find_user
from source.model.blockchain import Blockchain, Transaction, generate_private_and_public_key
import time
import getpass
from termcolor import colored
from Crypto.PublicKey import ECC
from login import login
from prompt_toolkit import prompt
import os


def generate_public_and_private_key_for_user(username):
    time.sleep(1)
    print("We need to generate a public and private key for you")
    print()

    time.sleep(1)
    print("Generating...")
    time.sleep(2)

    user_private_key, user_public_key = generate_private_and_public_key()

    user_public_key = user_public_key.export_key(format='OpenSSH')

    print(f"Your public key is: {user_public_key}")
    print()
    time.sleep(1)
    store_public_key(username, user_public_key)
    print(colored("We automatically stored it for you!", "green"))

    print()
    private_key_passphrase = getpass.getpass(
        "Enter the passphrase for your private key: ").replace(" ", "")
    print()
    time.sleep(1)

    print(colored("Attention! if you lose your passphrase you will not be able to make transactions in your account", "yellow"))
    print(colored("Store your private key in some safe place!", 'yellow'))

    print()

    user_private_key = user_private_key.export_key(
        format='PEM', passphrase=private_key_passphrase, protection='PBKDF2WithHMAC-SHA1AndAES128-CBC')

    print(colored("Copy the \"-----BEGIN ENCRYPTED PRIVATE KEY-----\" and \"-----END ENCRYPTED PRIVATE KEY-----\"", "yellow"))

    print()

    print(f"Your private key is: {user_private_key}")
    print()
    result = change_public_and_private_key_status(username, user_public_key)

    input("[PRESS ENTER TO CONTINUE]")

    return result


def add_transaction_to_current_data(username, blockchain):
    print()
    print("You choosed to add a new transaction.")
    print()
    time.sleep(1)
    sentinel = ''
    user_private_key = prompt("Type your private key (press [Meta+Enter] or [Esc] followed by [Enter] to accept the input): \n\n", multiline=True)
    time.sleep(1)
    print()
    passphrase = getpass.getpass("Type the passphrase for your private key: ").replace(" ", "")
    print()

    recipient_public_key = input("Type the recipient CryptoCoin address of the transaction: ").replace(" ", "")
    print()
    time.sleep(1)

    value = int(input("Type the value of the transaction: "))
    time.sleep(1)

    sender_public_key = get_public_key(username)

    sender_public_key = ECC.import_key(sender_public_key)
    sender_private_key = ECC.import_key(user_private_key, passphrase=passphrase)

    transaction = Transaction(sender_public_key, recipient_public_key, sender_private_key, value)

    public_transaction = transaction.sign_transaction()

    # Deleting the private key from the transaction for security purposes
    delattr(transaction, 'sender_private_key')

    blockchain.add_transaction(public_transaction)
    time.sleep(1)

    print()
    print(colored('Transaction successfully registered!', 'green'))

    os.system('cls||clear')

    return True

def view_wallet(username):
    print()
    print("You choosed to see your wallet")
    print()
    time.sleep(1)
    print(f"Your currently have {float(get_balance(username))} CRCs")
    print()
    time.sleep(1)
    print(f"Your public key is {get_public_key(username)}")
    time.sleep(1)
    print()
    input("[PRESS ENTER TO CONTINUE]")
    if get_public_key(username) == None:
        return False
    return True


def app():
    status, username = login()
    if status == True:
        os.system('cls||clear')
        blockchain = Blockchain()
        print()
        time.sleep(1)
        print(
            '-' * 30 + f' Welcome to the Cryptocoin, {username}! ' + "-" * 30)
        while True:
            if get_public_and_private_key_status(username) == 0:
                generate_public_and_private_key_for_user(username)
                os.system('cls||clear')
            elif get_public_and_private_key_status(username) == 1:
                while True:
                    print()
                    time.sleep(1)
                    print('Choose between the options below:')
                    time.sleep(1)
                    print()
                    print('[1]: Make a new transaction')
                    time.sleep(1)
                    print('[2]: View your wallet')
                    time.sleep(1)
                    print('[3]: Quit')
                    time.sleep(1)
                    while True:
                        print()
                        choice = int(getpass.getpass('Type: '))
                        if choice <= 3 and choice > 0:
                            break
                        else:
                            print()
                            print(
                                colored("Invalid value! Answer only 1, 2 or 3!", "red"))
                    if choice == 1:
                        add_transaction_to_current_data(username, blockchain)
                    if choice == 2:
                        view_wallet(username)
                    if choice == 3:
                        os.system('cls||clear')
                        time.sleep(1)
                        text = f"Goodbye, {username}!"
                        print(colored(text, 'green'))
                        time.sleep(1)
                        os.system('cls||clear')
                        return True
    else:
        print(colored("Error during login", "red"))
        return False

if __name__ == '__main__':
    app()