from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    app_secret: str

    settlement_url: str
    settlement_username: str
    settlement_token: str

    merchant_id: str
    base_qr_string: str
    logo_path: str

    class Config:
        env_file = ".env"

settings = Settings(
    database_url = None,
    app_secret = None,
    settlement_url = None,
    settlement_username = None,
    settlement_token = None,
    merchant_id = None,
    base_qr_string = None,
    logo_path = None,
)
