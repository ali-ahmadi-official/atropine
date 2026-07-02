import requests
import random

USERNAME = "username"
PASSWORD = "password"
FROM = "5000xxxx"

def generate_code():
    return str(random.randint(100000, 999999))

def send_sms(mobile, code):
    url = (
        "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
    )

    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "to": mobile,
        "from": FROM,
        "text": f"کد ورود شما به آتروپین : {code}",
        "isflash": False
    }

    requests.post(url, json=payload)
