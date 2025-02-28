import os 
from pathlib import Path
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.core.mail import send_mail
import random




def generate_otp_code():
    return ''.join(random.choices('0123456789', k=6)) #générer un code otp de 6 chiffres


def send_otp_email(email, otp_code):
	subject = 'Transcendence - Two Factor Authentication'
	message = f'Your OTP code is {otp_code}.'
	from_email = 'noreply.4.2.1.2.3@gmail.com'
	recipient_list = [email] #envoyer un email avec le code otp
	send_mail(subject, message, from_email, recipient_list) #envoyer un email avec le code otp