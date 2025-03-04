import json

import pyotp
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.environment import XAI_API_KEY
from app.forms import PortfolioGenerationForm, PortfolioReviewForm
from app.prompts import (
    portfolio_generation_system_prompt,
    portfolio_generation_user_query,
    portfolio_review_system_prompt,
    portfolio_review_user_query,
)


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


def get_llm_response(form: PortfolioReviewForm | PortfolioGenerationForm):
    client = OpenAI(
        base_url="https://api.x.ai/v1",
        api_key=XAI_API_KEY,
    )

    if isinstance(form, PortfolioGenerationForm):
        system_prompt = portfolio_generation_system_prompt()
        user_query = portfolio_generation_user_query(form)
    elif isinstance(form, PortfolioReviewForm):
        system_prompt = portfolio_review_system_prompt()
        user_query = portfolio_review_user_query(form)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
