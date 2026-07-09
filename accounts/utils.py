import requests
import random

def generate_code():
    return str(random.randint(100000, 999999))

URL = "https://console.melipayamak.com/api/send/simple/ee4033b63f624bf1bc9edbce94d5ff19"

def send_sms(mobile, text):
    url = URL

    payload = {
        "from": "50004001586578",
        "to": mobile,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)

        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)

        return response.json()

    except Exception as e:
        print("Error:", e)


# import requests

# data = {'to': '09938285221'}
# response = requests.post('https://console.melipayamak.com/api/send/otp/ee4033b63f624bf1bc9edbce94d5ff19', json=data)
# print(response.json())