import secrets
import requests
import jwt
import hashlib

AUTHSECRET = "SecureNoAzazaza"
class ServiceList:
    _service_url_list: list = ["localhost:8001"]#todo вообще, это в конфигах должно быть, ip/host/port!


    @classmethod
    def get_service_list(cls) -> list:
        return cls._service_url_list

def code_password(password: str, thin, shape, length):
    return f"{thin}000{shape}111{length}{hashlib.sha256(password)}"
def generate_authsecret():
    return secrets.token_urlsafe(16)

def post_services_authsecret(secret: str):
    for sevice_url in ServiceList.get_service_list():
        encoded_secret_jwt = jwt.JWT.encode({"service_key": secret},
                                            AUTHSECRET,
                                            algorithm='HS256')
        requests.post(f"{sevice_url}/update_key", {"service_key": encoded_secret_jwt})