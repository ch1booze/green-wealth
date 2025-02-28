import secrets

from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.environment import SENDGRID_API_KEY, XAI_API_KEY


def generate_otp():
    return str(secrets.randbelow(1000000)).zfill(6)


def send_otp_email(email, otp):
    message = Mail(
        from_email="your_email@example.com",
        to_emails=email,
        subject="Your OTP",
        html_content=f"Your OTP is: <strong>{otp}</strong>",
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def initialise_llm():
    client = OpenAI(
        base_url="https://api.x.ai/v1",
        api_key=XAI_API_KEY,
    )
    return client


def generate_prompt_for_portfolio_generation(): ...


def generate_prompt_for_portfolio_review(): ...


def portfolio_generator():
    llm = initialise_llm()


def portfolio_reviewer(): ...
