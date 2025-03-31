## About

This project is a port of Luca Mingarelli's [cryptpandas](https://github.com/LucaMingarelli/CryptPandas) package and allows 
users to easily **encrypt and decrypt numpy arrays** in addition to pandas dataframes.


## Installation

You can install `cryptnumpy` with pip:

`pip install cryptnumpy`

### NumPy example

You can encrypt and decrypt a single *numpy array* as follows:

```python
import numpy as np
import cryptnumpy as crp

my_array = np.arange(10)

crp.to_encrypted(my_array, password='APassWord', path='file.crypt')
decrypted_array = crp.read_encrypted('file.crypt', password='APassWord')

print(np.all(my_array == decrypted_array))
```

A *dictionary of numpy arrays* works just the same:

```python
import numpy as np
import cryptnumpy as crp

my_array_dict = dict(
    arry1=np.array(['foo', 'bar', 'baz']),
    arry2=np.array(['qux', 'quux'])
)

crp.to_encrypted(my_array_dict, password='APassWord', path='file.crypt')
decrypted_dict = crp.read_encrypted('file.crypt', password='APassWord')

for name, original_array in my_array_dict.items():
    decrypted_array = decrypted_dict[name]
    print(np.all(original_array == decrypted_array))
```

### Pandas example

For convenience, `cryptnumpy` maintains the original functionality of Luca Mingarelli's `cryptpandas` package. 
Specifically, you can encrypt and decrypt a *pandas dataframe* as follows:

```python
import pandas as pd
import cryptnumpy as crp

my_df = pd.DataFrame(
    {'A': [1, 2, 3],
     'B': ['foo', 'bar', 'baz']
     }
)

crp.to_encrypted(my_df, password='somePassword', path='file.crypt')
decrpyted_df = crp.read_encrypted(
    'file.crypt', 
    password='somePassword', 
    use_pandas=True 
)
print(decrpyted_df.equals(my_df))
```
By default, the `read_encrypted` function will assume that your encrypted data is a **numpy array**. 
To load an encrypted dataframe instead, you need to set `use_pandas=True` (see above).  

If you are *only* looking to encrypt and decrypt dataframes, and do not need support for 
numpy arrays, you should install the original `cryptpandas` package. `cryptnumpy` will not offer 
you any additional functionalities in that case.   

### Requirements

-   `pandas`
-   `numpy`
-   `cryptography >= 41.0.4`
-   `pyarrow >= 14.0.1`

### Licence

[MIT](LICENSE.txt)
