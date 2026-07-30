import requests
import random

TOKEN = "tokenQeuykplnvnws"

URL = "https://atropine.ir/kiani/SMS/SendOTP.aspx"

def generate_code():
    return str(random.randint(100000, 999999))

def send_sms(mobile, code):
    try:
        response = requests.get(
            URL,
            params={
                "phone": mobile,
                "otp": code,
                "token": TOKEN,
            },
            timeout=10,
        )

        response.raise_for_status()

        result = response.text.strip()

        if result == "1":
            return {
                "success": True,
                "code": code,
            }

        return {
            "success": False,
            "error": result,
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "connection_error",
        }