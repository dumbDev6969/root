def encode_string(s):
    encoded = ""
    for char in s:
        encoded += chr(ord(char) + 1)
    return encoded

def decode_string(s):
    decoded = ""
    for char in s:
        decoded += chr(ord(char) - 1)
    return decoded