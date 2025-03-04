import json
import secrets
import pyotp
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.environment import DEEPSEEK_API_KEY, SESSION_SECRET

# from app.environment import SENDGRID_API_KEY, XAI_API_KEY


def generate_otp():
    totp = pyotp.TOTP("X4R4C7KUWIJK5QNIXB3KSFW2DZA3WDIV")
    return totp.now()


def verify_otp(otp: str):
    totp = pyotp.TOTP("X4R4C7KUWIJK5QNIXB3KSFW2DZA3WDIV")
    return totp.verify(otp)


def send_otp_email(email: str, otp: str):
    message = Mail(
        from_email="your_email@example.com",
        to_emails=email,
        subject="WealthWizard: Your OTP to login",
        html_content=f"Your OTP is: <strong>{otp}</strong>",
    )

    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def get_llm_response(system_prompt: str, user_query: str):
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=DEEPSEEK_API_KEY,
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
