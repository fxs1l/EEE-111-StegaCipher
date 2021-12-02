from PIL import Image
import os 

def load_image_data(filename):
    # Opens the image from the given filename
    image = Image.open(filename)
    # Gets the image dimensions of the image and saves it to the tuple size
    width, height = image.size
    size = (width, height)
    # Gets the values for image_data as a list
    image_data = list(image.getdata())
    return (size, image_data)

def save_image_to_file(filename, image_dimension, image_data):
    # Creates a new Image in RGB mode with given dimensions
    image = Image.new(mode = "RGB", size = image_dimension)
    # Puts image_data into the newly created Image
    image.putdata(image_data)
    # Saves the created Image into PNG format
    image.save(fp=filename, format='PNG')

def save_file(filename, text):
    # Saves the contents of text as filename
    with open(filename, "w") as f:
        f.write(text)

def get_data_to_encrypt(image_size):
    secret_key, message = '', ''
    image_size = image_size[0] * image_size[1] 

    def invalid_key(key):
        # Validity checklist for key: 
        # 1. Length is at least 3 and at most 20
        # 2. No invalid characters. Only "d" or "u" in key

        if 3 <= len(key) <= 20: # passed checklist no.1
            for k in key:
                if k == 'd' or k == 'u': # current character still passes checklist no.2
                    pass
                else: # failed checklist no.2, therefore invalid
                    return True
            return False # passed all validity checks, therefore valid 
        return True # failed checklist no.1, therefore invalid

    def invalid_message(message):
        # Validity checklist for message: 
        # 1. Length is at least 10 and at most 1000
        # 2. ASCII value for each character is at least 32 and at most 126

        if 10 <= len(message) <= 1000: # passed checklist no.1
            for m in message:
                if 32 <= ord(m) <= 126: # current character still passes checklist no.2
                    pass
                else: # failed checklist no.2, therefore invalid
                    return True
            return False # passed all validity checks, therefore valid
        return True # failed checklist no.2, therefore invalid

    while True:
        # Asks and validates secret_key and message
        while invalid_key(secret_key) or invalid_message(message):
            secret_key = str(input("Enter Key:"))
            message = str(input("Enter Message:"))
            # Checks if message and secret_key are valid, restarts the loop if invalid 
            if invalid_key(secret_key) or invalid_message(message):
                print("Invalid Key/Message. Please Try again.")
                secret_key, message = '', ''
        # Calculates the pixel size of secret_key and message
        characters = len(secret_key) + len(message)
        msg_key_size = int((characters * 8 )/3) + 7
        # Restarts the loop if Message and Key cannot fit
        if msg_key_size > image_size:
            print("Message and Key cannot fit in the image.")
            secret_key, message = '', ''
        else:
            break
    return (secret_key, message)

def encrypt_text(text, key):
    encrypted_text = ''
    key_len = len(key) # determines the number of shifts

    # Repeats the character pattern of key to iterate through the length of text
    if len(key) < len(text):
        repeat = len(text) // len(key) + 1
        key = key * repeat
    # Performs the actual encryption process
    for i in range(len(text)):
        ascii_char = ord(text[i])
        # Shifts the ASCII value down and retrieves its equivalent character
        if key[i] == 'd':
            # Makes the ASCII value at least 127 when shifting down makes it lesser than 32
            if ascii_char - key_len < 32: 
                ascii_char = ascii_char + 95 
            encrypted_char = chr(ascii_char - key_len)
        # Shifts the ASCII value up and retrieves its equivalent character
        elif key[i] == 'u':
            # Makes the ASCII value at least 31 when shifting up makes it greater than 126
            if ascii_char + key_len > 126:
                ascii_char = ascii_char - 95
            encrypted_char = chr(ascii_char + key_len)
        # Adds the encrypted character to encrypted_text
        encrypted_text = encrypted_text + encrypted_char
    return encrypted_text

def decrypt_text(encrypted_text, key):

    def invalid_key(key):
        # Validity checklist for key: 
        # 1. Length is at least 3 and at most 20
        # 2. No invalid characters. Only "d" or "u" in key

        if 3 <= len(key) <= 20: # passed checklist no.1
            for k in key:
                if k == 'd' or k == 'u': # current character still passes checklist no.2
                    pass
                else: # failed checklist no.2, therefore invalid
                    return True
            return False # passed all validity checks, therefore valid 
        return True # failed checklist no.1, therefore invalid

    def invalid_message(message):
        # Validity checklist for message: 
        # 1. Length is at least 10 and at most 1000
        # 2. ASCII value for each character is at least 32 and at most 126

        if 10 <= len(message) <= 1000: # passed checklist no.1
            for m in message:
                if 32 <= ord(m) <= 126: # current character still passes checklist no.2
                    pass
                else: # failed checklist no.2, therefore invalid
                    return True
            return False # passed all validity checks, therefore valid
        return True # failed checklist no.2, therefore invalid
        
    # Checks if the encrypted_text or key are valid and exits the function if invalid
    if invalid_message(encrypted_text) or invalid_key(key):
        return None
    decrypted_text = ''
    original_key_len = len(key)
    # Repeats the character pattern of key to iterate through the length of text
    if len(key) < len(encrypted_text): 
        repeat = len(encrypted_text) // len(key) + 1
        key = key * repeat
    # Performs the actual decryption process
    for i in range(len(encrypted_text)):
        ascii_char = ord(encrypted_text[i])
        # Shifts the ASCII value down and retrieves its equivalent character
        if key[i] == 'u':
            if ascii_char - original_key_len < 32:
                ascii_char = ascii_char + 95
            decrypted_char = chr(ascii_char - original_key_len)
        # Shifts the ASCII value up and retrieves its equivalent character
        elif key[i] == 'd':
            if ascii_char + original_key_len > 126:
                ascii_char = ascii_char - 95
            decrypted_char = chr(ascii_char + original_key_len)
        # Adds the decrypted character to decrypted_Text
        decrypted_text = decrypted_text + decrypted_char
    return decrypted_text 

def char_to_ascii(word):
    # Converts each character in word to its ASCII value
    ascii_values = []
    for i in word:
        ascii_values.append(ord(i))
    return ascii_values

def ascii_to_binary(ascii_values):
    # Converts the ASCII values to binary
    binary_values = []
    for i in ascii_values:
        # Using .zfill(8) ensures that the binary has enough leading 
        # zeroes to make its length 8 bits
        binary_string = str(bin(i))[2:].zfill(8) 
        binary_values.append(binary_string)
    return binary_values

def binary_to_ascii_string(binary_values):
    # Converts the binaries back to their equivalent ASCII values
    ascii_string = ''
    for i in binary_values:
        ascii_string += chr(int(i, 2))
    return ascii_string

def encode_message(image_data, binary_key, binary_encrypted_message):
    index, bytes_encoded = 0, 0
    modified_data = []

    # Helper function to modify RGB values. 
    # The same 10 lines of code below was used for 4 different conditions, thus this inner function
    def modify_rgb(rgb, bit):
        # +1 to RGB value if desired bit is 0 and rgb is odd
        if bit == '0' and rgb % 2 != 0: 
            if rgb == 0: # minimum RGB value is 0 so cycle back to 255
                rgb = 255
            else:
                rgb -= 1
        # -1 RGB value if desired bit is 1 and rgb is even
        elif bit == '1' and rgb % 2 == 0:
                rgb += 1
        return rgb

    for pv in image_data:
        modified_pv = ()
        for rgb in pv:
            # Encode the elements in binary_key
            if bytes_encoded < len(binary_key):
                rgb = modify_rgb(rgb, binary_key[bytes_encoded][index])
            # Encode the delimiter
            elif  len(binary_key) == bytes_encoded:
                rgb = modify_rgb(rgb, '1')
            # Encode the elements in binary_encrypted_message
            elif len(binary_key) < bytes_encoded < len(binary_key) + len(binary_encrypted_message) + 1:
                rgb = modify_rgb(rgb, binary_encrypted_message[bytes_encoded-len(binary_key)-1][index])
            # Encode the second delimiter 
            elif len(binary_key) + len(binary_encrypted_message) + 1 == bytes_encoded:
                rgb = modify_rgb(rgb, '1')
            # Update counters and note if 8 bits have been encoded
            if index == 7: 
                index = 0
                bytes_encoded += 1
            else:
                index += 1
            # Saves the modified pixel values 
            modified_pv = modified_pv + (rgb,)
        modified_data.append(modified_pv)
    return modified_data

def decode_message(image_data):
    binary_key, binary_encrypted_message, binaries, eight_bit = [], [], [], ''
    # Decodes the bits and appends them to binaries
    for pv in image_data:
        for rgb in pv:
            # Determines if bit is zero or one based on rgb if it's even or odd 
            if rgb % 2 != 0:
                bit = 1
            else:
                bit = 0
            eight_bit += str(bit)
            # Adds eight_bit to binaries every 8 bits
            if len(eight_bit) == 8:
                binaries.append(eight_bit)
                eight_bit = ''
    # Returns an error if no delimiters were found
    if binaries.count('11111111') == 0 : 
        return (None, None)
    # Distributes the elements in binaries to binary_key and binary_encrypted_message         
    delimiters = 0
    for b in binaries:
        if b == '11111111':
            delimiters += 1
        else:
            if delimiters == 0: # no delimiters yet, so it must be part of the key
                binary_key.append(b)
            elif delimiters == 1: # first delimiter found, so it must be part of the message
                binary_encrypted_message.append(b)
    # Returns an error if image data does not contain a message
    if len(binary_encrypted_message) == 0:
        return (None, None)
    return (binary_key, binary_encrypted_message)

def main():
    mode = ''
    filename = ''
    while mode != 'exit':
        mode = input("Select program mode (encrypt/decrypt/exit):")
        if mode == 'exit':
            print("Thank you for using this program!")
            break
        elif mode == 'encrypt' or mode == 'decrypt':
            # Asks and validates inputted filename
            while not os.path.isfile(filename):
                filename = input("Enter image filename:")
                if not os.path.isfile(filename) or not filename.lower().endswith((".jpg",".jpeg")): 
                    print("Invalid image file.")
                    filename = ''
            # Once a valid image file is inputted, loads the image size and the image data
            size, image_data = load_image_data(filename)
            if mode == 'encrypt':
                # Asks user for the Message and Key to encrypt
                data = get_data_to_encrypt(size)
                # Converts key and encrypted message to binary
                binary_key = ascii_to_binary(char_to_ascii(data[0]))
                binary_encrypted_message = ascii_to_binary(char_to_ascii(encrypt_text(data[1], data[0])))
                # Encodes the key and encrypted message to image_data 
                modified_image_data = encode_message(image_data, binary_key, binary_encrypted_message)
                # Modifying the filename using os module methods to meet SP1 specs
                filename = os.path.join("output", "modified_" + os.path.basename(filename))
                # Saves the modified image_data to the new filename
                save_image_to_file(filename, size, modified_image_data)
            else:
                decode_erorr = "Error: cannot decode message!"
                # Decodes the binaries found in image_data
                binaries = decode_message(image_data)
                if binaries[0] is not None:
                    key, encrypted_message = binary_to_ascii_string(binaries[0]), binary_to_ascii_string(binaries[1])
                    decrypted_text = decrypt_text(encrypted_message, key)
                    if decrypted_text is not None:
                        # Modifes the filename with os module methods and then saves the file
                        filename = os.path.join("output", os.path.basename(filename).split('.')[0] + "_decoded_message.txt")
                        save_file(filename, decrypted_text)
                    # Decode error so resetting to asking for program mode
                    else:
                        print(decode_erorr)
                        mode = ''
                # Decode error so resetting to asking for program mode
                else:
                    print(decode_erorr)
                    mode = ''
            filename = ''
        else:
            print("Invalid input, choose a different item!")
            mode = ''

if __name__ == "__main__":
    main()