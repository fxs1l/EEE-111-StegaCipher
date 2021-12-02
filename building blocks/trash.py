
# def decode_message(image_data):
#     delimiter_index = 0
#     binary_key, binary_encrypted_message, byte_key, byte_message = [], [], '', ''
#     for pv in image_data:
#         for rgb in pv:
#             if delimiter_index < 8: # First delimiter still not yet decoded
#                 bit, delimiter_index = get_bit(rgb, delimiter_index)
#                 byte_key += str(bit)
#                 # Adds byte_key to binary_key every 8 bits
#                 if len(byte_key) == 8:
#                     binary_key.append(byte_key)
#                     byte_key = ''         
#             elif 8 < delimiter_index < 16: # Second delimiter still not yet decoded
#                 bit, delimiter_index = get_bit(rgb, delimiter_index) 
#                 byte_message += str(bit)
#                 # Adds byte_message to binary_encrypted_message every 8 bits 
#                 if len(byte_message) == 8:
#                     binary_encrypted_message.append(byte_message)
#                     byte_message = ''
#     # Shows error messages
#     # or (7 <= delimiter_index < 16 and len(byte_key) < 8)
#     if delimiter_index < 7 :
#         print("Error: cannot decode message!")
#         return 0,0
#     else:
#         return binary_key, binary_encrypted_message