# protectionstnd

This package proporcionates the capability of detecting sql injection in your json/dict data.
Regardles of how your data looks like and how nested is your dictionary, it will go through 
each step and provide a response

Usage:

import libs

```python 
import protectionstnd
```

for validating a dictionary in case a sql injection has been mada

```python 
dict_to_check = {"one": {"second": "ssss"}}
protectionstnd.sql.sql_check(dict_to_check)
```

for analyzing a dict and receive more detailed information, how many sql injections has been detected
```python 
dict_to_check = {"one": {"second": "ssss"}}
protectionstnd.sql.sql_analizer(dict_to_check)
```

RUT/RUN checker for CHILE
```python 

protectionstnd.cl.rut_run_checker("123456789-2")
```