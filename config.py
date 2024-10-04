# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    TWILIO_NUMBER= os.environ.get('TWILIO_NUMBER')
    TWILIO_ACCOUNT_SID= os.environ.get('TWILIO_ACCOUNT_SID')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False