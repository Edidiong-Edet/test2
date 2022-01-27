

# from werkzeug import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from flaskext.mysql import MySQL
from config import app

import datetime

import pymysql.cursors

load_dotenv()




 
 # db = SQLAlchemy(app)

mysql = MySQL()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
SALT=os.getenv('SALT')
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('DBUSER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DBPASS')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB')
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-05.cleardb.net'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)



	

""" class Signup(db.Model):
  __tablename__ = 'articles'
  User_id = db.Column(db.Integer, primary_key = True)
  First_name = db.Column(db.String(300))
  Last_name = db.Column(db.String(300))
  Email = db.Column(db.String(60))
  Password = db.Column(db.String(255))
  
  def __init__(self, User_id,First_name,Last_name,Email,Password):
    self.User_id = User_id
    self.First_name = First_name 
    self.Last_name = Last_name
    self.Email = Email
    self.Password = Password """
   

