import io
from pickle import UnpicklingError

import numpy as np
import pandas as pd
import pytest
from cryptography.fernet import InvalidToken
from pyarrow.lib import ArrowInvalid

import cryptnumpy as crp

df = pd.DataFrame({"A": [1, 2, 3], "B": ["foo", "bar", "baz"]})
arr = np.arange(25).reshape(5, 5)
arr_dict = dict(a=np.array(["foo", "bar"]), b=np.linspace(0, 10))


def test_get_key():
    from cryptnumpy.encrypt_decrypt import DEFAULT_SALT

    key = crp.encrypt_decrypt._get_key(password="ApassWord", salt=DEFAULT_SALT)
    key_val = b"mn68JONFMiJhvbi5mcQ1pzwWYA7mysfDg2w_IaXjwBo="
    assert key == key_val


def test_make_salt():
    from cryptnumpy import make_salt

    assert len(make_salt(__size=124)) == 124


def _write_read_file_path_df(path, pwd, salt):
    crp.to_encrypted(df, pwd, path, salt)
    decrypted = crp.read_encrypted(path, pwd, salt, use_pandas=True)
    assert df.equals(decrypted)


def _write_read_file_path_array(path, pwd, salt):
    crp.to_encrypted(arr, pwd, path, salt)
    decrypted = crp.read_encrypted(path, pwd, salt)
    assert np.all(arr == decrypted)


def _write_read_file_path_array_dict(path, pwd, salt):
    crp.to_encrypted(arr_dict, pwd, path, salt)
    decrypted = crp.read_encrypted(path, pwd, salt)
    assert set(arr_dict.keys()) == set(decrypted.keys())
    for file in arr_dict:
        assert np.all(arr_dict[file] == decrypted[file])


def test_write_read_df_no_salt():
    _write_read_file_path_df(path="file.crypt", pwd="verySecret", salt=None)


def test_write_read_df_with_salt():
    from cryptnumpy import make_salt
    my_salt = make_salt(32)
    _write_read_file_path_df(path="file.crypt", pwd="alsoSecret", salt=my_salt)


def test_write_read_array_no_salt():
    _write_read_file_path_array(path="file.crypt", pwd="anotherSecret", salt=None)


def test_write_read_array_with_salt():
    from cryptnumpy import make_salt
    my_salt = make_salt(32)
    _write_read_file_path_array(path="file.crypt", pwd="Password", salt=my_salt)


def test_write_read_array_dict_no_salt():
    _write_read_file_path_array_dict(path="file.crypt", pwd="anotherPwd", salt=None)


def test_write_read_array_dict_with_salt():
    from cryptnumpy import make_salt
    my_salt = make_salt(32)
    _write_read_file_path_array_dict(path="file.crypt", pwd="oneMorePwd", salt=my_salt)


def test_write_read_with_buffer_df():
    pwd = "secretPhrase"

    path = io.BytesIO()
    crp.to_encrypted(df, password=pwd, path=path)
    path.seek(0)
    decrypt_df = crp.read_encrypted(password=pwd, path=path, use_pandas=True)
    assert df.equals(decrypt_df)


def test_write_read_with_buffer_array():
    pwd = "topSecret"

    path = io.BytesIO()
    crp.to_encrypted(arr, password=pwd, path=path)
    path.seek(0)
    decrypted = crp.read_encrypted(password=pwd, path=path)
    assert np.all(arr == decrypted)


def test_read_no_password_fails_df():
    crp.to_encrypted(df, password="forgottenPassword", path="file.crypt")
    with pytest.raises(ArrowInvalid):
        pd.read_parquet("file.crypt")


def test_read_no_password_fails_array():
    crp.to_encrypted(arr, password="forgottenPassword", path="file.crypt")
    with pytest.raises(UnpicklingError):
        np.load("file.crypt", allow_pickle=True)
    with pytest.raises(ValueError):
        np.load("file.crypt")


def test_read_wrong_password_fails_df():
    crp.to_encrypted(df, password="realPassword", path="file.crypt")
    with pytest.raises(InvalidToken):
        crp.read_encrypted(password="wrongPassword", path="file.crypt", use_pandas=True)


def test_read_wrong_password_fails_array():
    crp.to_encrypted(arr, password="realPassword", path="file.crypt")
    with pytest.raises(InvalidToken):
        crp.read_encrypted(password="wrongPassword", path="file.crypt")
