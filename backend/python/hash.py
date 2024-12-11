import hashlib
import smtplib
server=smtplib.SMTP(host="smtp.gmail.com",port=587)


# server.starttls()
# server.login(user="jem_022190@binalatongan.edu.ph",
# password=)
# to_email=["jemcarlo46@gmail.com"]

# Prompt the user for input
user_input ="jem_022190@binalatongan.edu.ph"

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

# Example usage
original = "szdx ibeh tpzj wmwp"
encoded = encode_string(original)
decoded = decode_string(encoded)

# print(f"Original: {original}")
print(f"Encoded: {encoded}")
print(f"Decoded: {decoded}")
#09e79ad7b4b9391ed7ff530266c9e831
#858033ed980e56ee3d52819593f09de0
email="kfn`1332:1Acjobmbupohbo/fev/qi"
password = "szdx ibeh tpzj wmwp"
