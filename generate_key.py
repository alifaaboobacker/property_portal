from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save it to a file
with open('key.key', 'wb') as key_file:
    key_file.write(key)
