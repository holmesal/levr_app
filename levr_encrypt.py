from Crypto.Cipher import ARC4
from levr_encrypt_data import encryption_key, password_encryption_key
import base64



def encrypt_password(pw):
	pw = str(pw)
	obj1 = ARC4.new(password_encryption_key)
	cipher_pw = obj1.encrypt(pw)
	url_safe_pw = base64.urlsafe_b64encode(cipher_pw)
	return str(url_safe_pw)

def encrypt_key(key):
	key = str(key)
	obj1 = ARC4.new(encryption_key)
	cipher_key = obj1.encrypt(key)
	url_safe_key = base64.urlsafe_b64encode(cipher_key)
	return str(url_safe_key)

def decrypt_key(url_safe_key):
	url_safe_key = str(url_safe_key)
	cipher_key = base64.urlsafe_b64decode(url_safe_key)
	obj2 = ARC4.new(encryption_key)
	key = obj2.decrypt(cipher_key)
	return str(key)
