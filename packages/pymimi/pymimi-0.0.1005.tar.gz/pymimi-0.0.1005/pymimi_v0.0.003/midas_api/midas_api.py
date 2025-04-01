import requests

_BASE_URL = None
_MAPI_KEY = None

def url_cfg(base_url: str, mapi_key: str,test:int=0):
    global _BASE_URL, _MAPI_KEY
    _BASE_URL = base_url
    _MAPI_KEY = mapi_key
    # print("MidasAPI:", _BASE_URL, _MAPI_KEY)
    if test == 1:
        print("MidasAPI:", _BASE_URL, _MAPI_KEY)
    else:
        pass

def midasapi(method:str, command:str,body=None):
    if not _BASE_URL or not _MAPI_KEY:
        raise ValueError("请先调用 url_cfg(base_url, mapi_key) 来设置API连接"
                         "Call url_cfg(base_url, mapi_key) first to set credentials")

    url = _BASE_URL + command

    headers = {
        "Content-Type": "application/json",
        "MAPI-Key": _MAPI_KEY
    }

    if method == "POST":
        response = requests.post(url=url, headers=headers, json=body)
    elif method == "PUT":
        response = requests.put(url=url, headers=headers, json=body)
    elif method == "GET":
        response = requests.get(url=url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url=url, headers=headers)

    # print(method, command, response.status_code)
    return method,command,response.status_code

def test_url(x:int = 0):
    if x == 1:
        method, command, response = midasapi("POST", "/doc/new", {})
        if response == 200:
            print("你的url和api配置正确，已连接成功！")
        elif response != 200:
            raise ValueError(response)
    else:
        pass


