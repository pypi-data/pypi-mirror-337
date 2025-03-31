"""
Port of `cryptpandas` which adds support for the encryption and decryption
of numpy arrays in addition to pandas dataframes.

Original `cryptpandas` author: Luca Mingarelli (https://github.com/LucaMingarelli)
Adding numpy support: S. Langenbach (ETHZ)
"""

import base64
import io
import os

import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DEFAULT_SALT = b'\xb6\xd2.B\xef\xbd\x11\xd3-\xd0\nV\xdd\x10\x93L'


def make_salt(__size=16):
    """
    Make a new salt.

    Args:
        __size (int): desired size of salt

    Returns: salt of size `__size`.
    """
    return os.urandom(__size)


def _get_key(password, salt=None):
    """
    Generate secret key associated with provided password.

    Args:
        password (str): Your password or passphrase.
        salt: The salt; if `None` (default) uses a default salt.
    """
    enpassword = password.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt or DEFAULT_SALT,
                     iterations=100_000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(enpassword))   # you can use kfd only once
    return key


def to_encrypted(data, password, path, salt=None):
    """
    Write a numpy array, dictionary of numpy arrays, or a pandas.DataFrame
    to a password encrypted file.

    Args:
       data (np.ndarray, Dict[str, np.ndarray], or pandas.DataFrame): The data to be encrypted.
       password (str): Unique password or passphrase.
       path (str, Path, or io.BytesIO): Path where the encrypted file should be saved.
       salt:  Salt for data encryption; if `None` (default) uses a default salt.
    """
    key = _get_key(password, salt=salt)
    fernet = Fernet(key)

    # serialise
    fstream = io.BytesIO()
    if isinstance(data, pd.DataFrame):
        data.columns = data.columns.astype(str)
        data.to_parquet(fstream)  # type: ignore
    elif isinstance(data, np.ndarray):
        np.save(fstream, data)  # type: ignore
    elif isinstance(data, dict) and all(isinstance(v, np.ndarray) for v in data.values()):
        np.savez(fstream, **data)  # type: ignore
    else:
        raise ValueError(
            "Unsupported type. `data` must be a pandas.DataFrame, "
            "np.ndarray, or dict of np.ndarray's."
        )

    # encrypt
    fstream.seek(0)
    encrypted_data = fernet.encrypt(fstream.read())

    # write
    if isinstance(path, io.BytesIO):
        path.write(encrypted_data)
    else:
        with open(path, 'wb') as file:
            file.write(encrypted_data)


def read_encrypted(path, password, salt=None, use_pandas=False):
    """
    Read a previously encrypted data file using numpy or pandas.

    Args:
       path (str, Path, or io.BytesIO): Path from which to read the encrypted file.
       password (str): Unique password used to encrypt the file.
       salt: Salt for data encryption; if `None` (default) uses a default salt.
       use_pandas (bool): Whether to use pandas or numpy (default) to de-serialise the data.
    """

    # read
    if isinstance(path, io.BytesIO):
        encrypted_data = path.read()
    else:
        with open(path, 'rb') as file:
            encrypted_data = file.read()

    # decrypt
    key = _get_key(password, salt=salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)

    # deserialise
    fstream = io.BytesIO(decrypted)
    if use_pandas:
        return pd.read_parquet(fstream)
    return np.load(fstream)
