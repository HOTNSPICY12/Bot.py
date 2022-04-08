from base64 import b64encode, b64decode
from hashlib import sha1
from uuid import uuid4
import requests
import platform
import logging
import socket
import uuid
import json
import hmac
import re
from time import time
from typing import Union
api = "https://service.narvii.com/api/v1{}".format
tapjoy = "https://ads.tapdaq.com/v4/analytics/reward"


def c():
    return requests.get(f"https://ed-generators.herokuapp.com/device?data={time()}").text


def s(data: Union[str, dict]) -> str:
	response = requests.post("http://134.0.115.139/signature", json=data) 
	return response.text


def uu():
    return str(uuid4())
