from cryptography.fernet import Fernet
 
fernet = Fernet(Fernet.generate_key())