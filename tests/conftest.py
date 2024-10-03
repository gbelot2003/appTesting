# test/conftest.py

import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    TWILIO_NUMBER= os.environ.get('TWILIO_NUMBER')
    TWILIO_ACCOUNT_SID= os.environ.get('TWILIO_ACCOUNT_SID')