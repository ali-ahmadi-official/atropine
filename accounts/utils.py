import requests
import random

URL = "https://console.melipayamak.com/api/send/simple/ee4033b63f624bf1bc9edbce94d5ff19"

def generate_code():
    return str(random.randint(100000, 999999))

def send_sms(mobile, code):
    data = {
        "from": "50004001586578",
        "to": mobile,
        "text": f"دپارتمان مشاوره و منتورینگ آتروپین\n\nکد ورود شما: {code}\n\nاین کد را در اختیار دیگران قرار ندهید."
    }

    try:
        response = requests.post(URL, json=data)

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

        return {
            "code": code,
            "result": response.json()
        }

    except Exception:
        return None
