from typing import Optional
import requests


def height(address: str) -> (Optional[int], Optional[None]):
    try:
        response = requests.get(address)
        current_height = response.json()["block"]["header"]["height"] if "1317" in address else response.json()
        return int(current_height), None
    except (KeyError, TypeError, BaseException, ConnectionRefusedError) as error:
        return None, error
