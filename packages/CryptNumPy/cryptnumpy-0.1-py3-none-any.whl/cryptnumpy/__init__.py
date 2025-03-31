__about__ = "A tool for encryption and decryption of numpy arrays and pandas dataframes. Port of `cryptpandas`."
__version__ = '0.1'
__url__ = "https://github.com/lungoruscello/cryptnumpy"
__license__ = "MIT"
__author__ = "S. Langenbach"  # original `cryptpandas` author: Luca Mingarelli


from cryptnumpy.encrypt_decrypt import to_encrypted, read_encrypted, make_salt
