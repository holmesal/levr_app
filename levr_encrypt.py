from Crypto.Cipher import ARC4
import base64

encryption_key = 'chance'


def encrypt_password(pw):
	pass
def encrypt_key(key):
	print key
	obj1 = ARC4.new(encryption_key)
	print obj1
	cipher_key = obj1.encrypt(key)
	print cipher_key
	url_safe_key = base64.urlsafe_b64encode(cipher_key)
	return url_safe_key

def decrypt_key(url_safe_key):
	print url_safe_key
	cipher_key = base64.urlsafe_b64decode(url_safe_key)
	print cipher_key
	obj2 = ARC4.new(encryption_key)
	print obj2
	key = obj2.decrypt(cipher_key)
	return key
