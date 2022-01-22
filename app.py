
from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug import generate_password_hash, check_password_hash

from flaskext.mysql import MySQL

import datetime
from config import app

from modelsql import mysql

import pymysql.cursors
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for

from flask_cors import CORS, cross_origin


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
 
 # db = SQLAlchemy(app)


   
@app.route('/', methods=['GET'])
@cross_origin()
def show():
  return 'hello world'

@app.route('/sign-up', methods=['POST'])

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
          resp = jsonify('User added successfully!')
          resp.status_code = 200
          return resp
    else:
      return jsonify('worries')
  except Exception as e:
    
    print(e)
    
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


if __name__ == "__main__":
    app.run(debug = True)
