import inspect
from datetime import datetime
from tinydb import TinyDB

def get_caller_name():
    return inspect.stack()[2][3]


def dprint(param_name,param_value, log_file_name='./debug_db'):
    dttm_str = datetime.now().strftime("%d-%b-%Y - %H:%M:%S")
    db = TinyDB(f'{log_file_name}.json')
    calling_function = get_caller_name()
    log_dict={}
    log_dict["calling_from"] = calling_function
    log_dict["param_name"] = param_name
    log_dict["param_value"] = param_value
    log_dict["log_dttm"] = dttm_str
    db.insert(log_dict)
    db.close()
    return

def dprint2(script_name,execution_id,param_name,param_value,log_file_name='./debug_db'):
    dttm_str = datetime.now().strftime("%d-%b-%Y - %H:%M:%S")
    db = TinyDB(f'{log_file_name}-{execution_id}.json')
    calling_function = get_caller_name()
    log_dict={}
    log_dict["in_script"] = script_name
    log_dict["execution_id"] = execution_id
    log_dict["calling_from"] = calling_function
    log_dict["param_name"] = param_name
    log_dict["param_value"] = param_value
    log_dict["log_dttm"] = dttm_str
    db.insert(log_dict)
    db.close()
    return
