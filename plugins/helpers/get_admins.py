# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
from typing import Dict, List, Union

admins: Dict[int, List[int]] = {}


def set(chat_id: int, admins_: List[int]):
    admins[chat_id] = admins_


def get(chat_id: int) -> Union[List[int], bool]:
    if chat_id in admins:
        return admins[chat_id]

    return False