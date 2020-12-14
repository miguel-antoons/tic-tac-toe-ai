import cryptography.fernet as crypt


def create_key():
    """
    Generates a key in order to encrypt files, this key will be stored in the key.key file
    :return:
    """
    print("Creating encryption key...")
    key = crypt.Fernet.generate_key()
    with open("program_files\\key.key", "wb") as key_file:
        key_file.write(key)

    print("Done")


def load_key():
    """
    Returns the key in order to crypt/decrypt files
    :return: encryption key
    """
    return open("program_files/key.key", "rb").read()


def encrypt_file(filename):
    """
    Encrypts a file
    :param filename: file to encrypt
    :return: None
    """
    encryption_utility = crypt.Fernet(load_key())

    # reads the file to encrypt
    with open(filename, "rb") as file_to_encrypt:
        data_to_encrypt = file_to_encrypt.read()

    # encryption of the file
    encrypted_data = encryption_utility.encrypt(data_to_encrypt)

    # write the encrypted content in the file
    with open(filename, "wb") as file_to_encrypt:
        file_to_encrypt.write(encrypted_data)


def decrypt_file(filename):
    """
    Decrypts a file
    :param filename: file to decrypt
    :return: None
    """
    decryption_utility = crypt.Fernet(load_key())

    # reads the file to decrypt
    with open(filename, "rb") as file_to_decrypt:
        data_to_decrypt = file_to_decrypt.read()

    # decryption of the file
    decrypted_data = decryption_utility.decrypt(data_to_decrypt)

    # write the decrypted content in the file
    with open(filename, "wb") as file_to_decrypt:
        file_to_decrypt.write(decrypted_data)


if __name__ == "__main__":
    # decrypt_file("login.csv")
    # encrypt_file("login.csv")
    pass
