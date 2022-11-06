def vigenere(message, key):
    message = message.lower()
    message = message.replace(' ', '')
    len_key = len(key)
    cipher_text = ''

    for i in range(len(message)):
        letter = message[i]
        k = key[i % len_key]
        cipher_text = cipher_text + chr((ord(letter) - 97 + k) % 26 + 97)

    return cipher_text


if __name__ == '__main__':
    key = 'cryptii'
    key = [ord(letter) - 97 for letter in key]
    print(vigenere('The quick brown fox jumps over 13 lazy dogs.', key))
    # OUTPUT: vycfnqkmspdpvnqohjfxaqmcgxotcqwshoad
    
