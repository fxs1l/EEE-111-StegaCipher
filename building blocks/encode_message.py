def encode_message(image_data, binary_key, binary_encrypted_message):

    modified_data, modified_pixel, RGB, = [], (), []
    bits_encoded = 0
    delimiter = "11111111"
    
    # Represent all bits to encode as one string
    key_bits = "".join(map(str, binary_key))
    message_bits = "".join(map(str,binary_encrypted_message))
    bits = key_bits + delimiter + message_bits
    # Insert a second delimiter if image size permits
    if len(image_data) * 3  > len(bits):
        bits += delimiter
    # Get all RGB values as one list (removes the tuples)
    for pixel in image_data:
        for rgb in pixel:
            RGB.append(rgb)
    # Modify RGB values if desired bit is 0 and RG
    for rgb in RGB:                 
        if bits_encoded < len(key_bits):
            # +1 to RGB value if desired bit is 0 and rgb is odd
            if bits[bits_encoded] == '0' and rgb % 2 != 0: 
                if rgb == 0: # minimum RGB value is 0 so cycle back to 255
                    rgb = 255
                else:
                    rgb -= 1
            # -1 RGB value if desired bit is 1 and rgb is even
            elif bits[bits_encoded] == '1' and rgb % 2 == 0:
                rgb += 1
        bits_encoded +=1
        # Group every 3 bits into a tuple then append them to modified_data
        if bits_encoded % 3 == 0:
            modified_data.append(modified_pixel)
            modified_pixel = ()
        else:
            modified_pixel = modified_pixel + (rgb,)
    return modified_data

name = input("input text file: ")
# case = os.path.basename(name).split(".")[0][-2:]
with open(name, "r") as f:
    l = f.readlines()

a = l[0].strip().split(", (")
image_data = []
for i in a:
    for character in '()[]':
        i = i.replace(character,'')
    tup = ()
    for j in i.split(','):
        tup = tup + (int(j.strip()),)
    image_data.append(tup)

def get_binaries(line):
    b = line.strip().replace("[", "").replace("]", "").split(",")
    binary = []
    for i in b:
        binary.append(i.strip().replace("'", ""))
    return binary
binary_key = get_binaries(l[1])
binary_encrypted_message = get_binaries(l[2])
data = encode_message(image_data, binary_key, binary_encrypted_message)
print(data[0])