

# from werkzeug import generate_password_hash, check_password_hash

from flaskext.mysql import MySQL
from config import app

import datetime

import pymysql.cursors






 
 # db = SQLAlchemy(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'eddy'
app.config['MYSQL_DATABASE_PASSWORD'] = 'eddy'
app.config['MYSQL_DATABASE_DB'] = 'public'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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
   

