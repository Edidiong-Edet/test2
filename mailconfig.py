import os
from config import app
import smtplib
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()



EMAIL_USERNAME=os.getenv('EMAIL_USER')
EMAIL_PASSWORD=os.getenv('EMAIL_PASS')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
