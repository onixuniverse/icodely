from icodely.settings.default_settings import *
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("TOKEN")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")