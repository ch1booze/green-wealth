import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(env_var: str, default: str | None = None) -> str:
    if os.getenv(env_var) is None:
        if default is None:
            raise ValueError(f"Environment variable '{env_var}' is not set.")
        return default
    return os.environ[env_var]


DEEPSEEK_API_KEY = get_env_var("DEEPSEEK_API_KEY")
PORT = int(get_env_var("PORT", "5000"))
# SENDGRID_API_KEY = get_env_var("SENDGRID_API_KEY")
SESSION_SECRET = get_env_var("SESSION_SECRET")
# XAI_API_KEY = get_env_var("XAI_API_KEY")
