def decrypt_text(encrypted_text, key):
    decrypted_text = ''
    ### Do not modify anything above this line ###
    # insert your code here #
    if 0<=len(text)<=1000 and 0<=len(key)<=1000: # constraints
        if len(key) != 0:
            for k in key:
                if k == 'd' or k == 'u':
                    pass
                else:
                    return text

            original_key = len(key)

            if len(key) < len(text):
                repeat = len(text) // len(key) + 1
                key = key * repeat
            
            for i in range(len(text)):
                ascii_char = ord(text[i])
                if key[i] == 'u':
                    if ascii_char - original_key < 32:
                        ascii_char = ascii_char + 95
                    decrypted_char = chr(ascii_char - original_key)
                if key[i] == 'd':
                    if ascii_char + original_key > 126:
                        ascii_char = ascii_char - 95
                    decrypted_char = chr(ascii_char + original_key)
                decrypted_text = decrypted_text + decrypted_char                    
        else:
            return text

    ### Do not modify anything below this line ###
    return decrypted_text

if __name__ == "__main__":
    text = input()
    key = input()
    print(decrypt_text(text, key)) 
