# DEBUG2

This library helps in debug activity.

No more putting print in between lines of big scripts and trying to do the RCA.

The library helps you store the entries of each debug points, as effortlessly as print.

The entries are stored in json format.

The entries helps in creating a lineage of the script execution.

There are 2 available methods in this package :
- dprint
- dprint2

## dprint
This method is for simple use cases.

It takes 3 input parameters :
- param_name - the label for the parameter
- param_value - the value of the parameter
- file_name (optional) - for storing the entries in json format.

By default the file name for storing the entries is debug_db.json. Custom name and path can be provided.

## dprint2
This method is for advanced use cases.

It takes 5 input parameters :
- script_name - name of the script from which the call is made.
- execution_id - this is to keep the entries of each execution in separate files.
- param_name - the label for the parameter
- param_value - the value of the parameter
- file_name (optional) - for storing the entries in json format.

The json file is in the format of TinyDB, hence portable, and can be easy parsed, with each entries, with their own doc_id.


## Usage

Here is a simple example on how to use the package :

```python
from debug2 import debug2 as dbg
dbg_file_name ='123debug'

def add(a,b):
    return a+b
    
def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def avg(a,b):
    return (a+b)/2
    

if __name__ == "__main__":

    data = {"type":"credit",
            "balance":10000,
            "amount":200}

    if data["type"] == 'credit':
        balance = add(data["balance"],data["amount"])
        dbg.dprint("new_balance",balance)

        
    if data["type"] == 'debit':
        balance = sub(data["balance"],data["amount"])
        dbg.dprint("new_balance",balance,"debit")


```
