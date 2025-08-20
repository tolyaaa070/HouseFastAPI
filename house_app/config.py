import os
from dotenv import load_dotenv

from house_app.db.model import RefreshToken

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_LIFETIME = 30
REFRESH_TOKEN_LIFETIME = 3
