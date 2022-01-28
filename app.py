
from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug import generate_password_hash, check_password_hash
from config import app
from flaskext.mysql import MySQL
from flask_mail import Message
import jwt
import smtplib

import datetime
from itsdangerous import URLSafeTimedSerializer



from modelsql import mysql,JWT_SECRET_KEY,SALT
from mailconfig import mail


import pymysql.cursors
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for,make_response

from flask_cors import CORS, cross_origin


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
 
 # db = SQLAlchemy(app)


   
@app.route('/', methods=['GET'])
@cross_origin()
def show():
  return 'LEXANALYTICS DEV'

@app.route('/sign-up', methods=['POST'])
@cross_origin()
def add_user():
  try:
    _json = request.json
    firstname = _json['fname']
    lastname = _json['lname']
    email = _json['email']
    password = _json['pwd']
		# validate the received values
    if firstname and email and password and request.method == 'POST':
			#do not save password as a plain text
      hashed_password = generate_password_hash(password)
			# save edits
      
      sql = "INSERT INTO sign_up(First_Name,Last_Name,Email,Password) VALUES(%s, %s, %s,%s)"
      data = (firstname,lastname,email,hashed_password)
      conn = mysql.connect()
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      cursor.execute('SELECT * FROM sign_up WHERE Email= % s', (email, ))
      account = cursor.fetchone()
      if account:
         resp = jsonify('Account already exists')
         resp.status_code = 401
         return resp
       
      else:
          cursor.execute(sql, data)
          conn.commit()
          
          token = generate_confirmation_token(email)
          confirm_url = url_for('confirmemail', token=token, _external=True)
          html = render_template('email.html', confirm_url=confirm_url, user=firstname)
          
          sendmail(email,html)
          resp = jsonify('User added successfully!')
          resp.status_code = 200
          return resp
    else:
      resp = jsonify('Empty values in request')
      resp.status_code = 409
      return resp
  except Exception as e:
    
    print(e)
    
  finally:
    cursor.close() 
    conn.close()

@app.route('/basic_info', methods=['POST'])
@cross_origin()
def basicinfo():
  try:
    _json = request.json
    email = _json['Email']
    birthdate= _json['birthdate']
    gender = _json['gender']
    country = _json['country']
    state= _json['state']
    orgtype=_json['org_type']
    orgname=_json['org_name']
    role=_json['org_role']
    btdate=datetime.datetime.strptime(birthdate,"%d/%m/%Y")
    pydate=btdate.strftime('%Y-%m-%d')
    
    date=datetime.datetime.now()
    fdate=date.strftime('%Y-%m-%d %H:%M:%S')
    
		# validate the received values
    if email  and request.method == 'POST':
      sql = "INSERT INTO basic_info(Email,date_and_time_created,date_of_birth,gender,country,state) VALUES(%s, %s, %s, %s, %s, %s)"
      data = (email,fdate,pydate,gender,country,state)
      sql2 = "INSERT INTO legal_info(organization_type,name_of_organization,role_or_title,Email) VALUES(%s, %s, %s,%s)"
      data2 = (orgtype,orgname,role,email)
      conn = mysql.connect()
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      cursor.execute('SELECT * FROM basic_info WHERE Email= % s', (email, ))
      account = cursor.fetchone()
      if account:
         resp = jsonify('Account already exists')
         resp.status_code = 401
         return resp
       
      else:
          cursor.execute(sql, data)
          cursor.execute(sql2, data2)
          conn.commit()
          resp = jsonify('User Basic information added successfully!')
          resp.status_code = 200
          return resp
    else:
      resp = jsonify('Empty values in request')
      resp.status_code = 409
      return resp
  except Exception as e:
    
    print(e)
    
  finally:
    cursor.close() 
    conn.close()

@app.route('/user_details', methods=['POST'])
@cross_origin()
def userdetails():
  try:
    _json = request.json
    email = _json['Email']
		# validate the received values
    if email  and request.method == 'POST':
      conn = mysql.connect()
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      cursor.execute('SELECT basic_info.*, sign_up.* FROM basic_info INNER JOIN sign_up ON basic_info.EMAIL = sign_up.EMAIL WHERE sign_up.Email= % s', (email, ))
      account = cursor.fetchone()
      if account:
         resp = jsonify('User Exists')
         resp.status_code = 200
         return {'data':account}
       
      else:

        resp = jsonify('Account already exists')
        resp.status_code = 401
        return resp
    else:
      resp = jsonify('Empty values in request')
      resp.status_code = 409
      return resp
  except Exception as e:
    
    print(e)
    
  finally:
    cursor.close() 
    conn.close()


@app.route('/login', methods=['POST'])
@cross_origin()
def verify_user():
  try:
    _json = request.json
    email = _json['email']
    pwd = _json['pwd']
		# validate the received values
    if email and pwd and request.method == 'POST':
			#do not save password as a plain text
			# save edits
      conn = mysql.connect()
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      cursor.execute('SELECT * FROM sign_up WHERE Email= % s', (email, ))
      account = cursor.fetchone()
      if account:
        userid=account['Id']
        passw=account['Password']   
        if check_password_hash(passw, pwd):
          # jwt_token = generate_jwt_token(userid)
          token =generate_jwt_token(email)
          resp = jsonify('Password is correct')
          resp.status_code = 200
          return jsonify({'token' : token})
        else:        
          resp = jsonify('Wrong password')
          resp.status_code = 401 
          return resp 
      else:
          resp = jsonify('Email does not exist in database')
          resp.status_code = 401
          return resp
    else:
      resp = jsonify('Empty values in request or wrong request method used')
      resp.status_code = 409
      return resp
      
  except Exception as e:
    
    print(e)
    
  finally:
    cursor.close() 
    conn.close()

@app.route('/confirm/<token>')
def confirmemail(token):
  # return 'logged in'
  try:
    email = confirm_token(token)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM sign_up WHERE Email= % s', (email, ))
    account = cursor.fetchone()
    if account['Confirmed']:
      flash('Account already confirmed. Please login.', 'success')
    else:
     sql = "UPDATE sign_up SET Confirmed=%s WHERE Email=%s"
     data=(True,email)
     cursor.execute(sql, data)
     conn.commit()
     return'Account Confirmed'
  
  except:
    return'link has expired'
    
  finally:
    cursor.close() 
    conn.close()
  

@app.route('/cases')
def cases():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM case_header LIMIT 10")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()	


def generate_jwt_token(value):
    encoded_content = jwt.encode({
      'public_id':value,
      'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},
     JWT_SECRET_KEY,
     algorithm="HS256")
    return encoded_content

def sendmail(useremail,template):
  msg = Message('Lexanalytics Email Verification', sender =   'noreply@lexanalytics.io',html=template, recipients = [useremail])
  msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
  mail.send(msg)
  mail_resp = jsonify('Message Sent')
  mail_resp.status_code = 200
  return mail_resp

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(JWT_SECRET_KEY)
    return serializer.dumps(email, salt=SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(JWT_SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SALT,
            max_age=expiration
        )
    except:
        return False
    return email

if __name__ == "__main__":
    app.run(debug = True)
