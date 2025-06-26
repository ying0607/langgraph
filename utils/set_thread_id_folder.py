from datetime import datetime

# 模組第一次被 import 時就執行一次，並儲存到私有變數
_TODAY_DATE = datetime.today().strftime('%Y-%m-%d-%H-%M')

def get_today_date() -> str:
    """
    回傳本模組載入時算出的 today_date，
    同一個 runtime 中始終相同。
    """
    return _TODAY_DATE

# 看 memo.txt看 memo.txt
## thread id 
import contextvars

_thread_id_var = contextvars.ContextVar("thread_id", default=None)

def set_thread_id(thread_id: str) -> None:
    _thread_id_var.set(thread_id)

def get_userID_config(result: str):
    """
    根據 result 回傳 config dict 或純 thread_id。
    """
    thread_id = _thread_id_var.get()
    if result == "config":
        return {"configurable": {"thread_id": thread_id}}
    elif result == "id":
        return thread_id
    else:
        return None