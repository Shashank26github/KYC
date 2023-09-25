#import MySQLdb
import smtplib
import string
from email.mime.text import MIMEText
from random import random
import smtplib
from email.message import EmailMessage

import bcrypt
import pymysql
from app import app
from db_config import mysql
from flask import render_template, url_for
from flask import flash, request
from flask import flash, session, render_template, request, redirect


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('home.html', title='HOME - Landing Page')



@app.route('/pass')
def password():
    return render_template('pass.html')


#@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
#@app.route('/login', methods=['GET', 'POST'])
def login():
    global cursor
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        conn = mysql.connect()
        cursor = conn.cursor()
        stmt = "select * from employee where username=\"%s\" and password=\"%s\""%(username,password)
        sql1 = cursor.execute(stmt)
        sql1 = cursor.fetchone()
        if sql1:
            return render_template('employees.html', data=sql1)
        else:
            error = "Invalid Username or Password"
            return render_template('login.html', loginError=error)
    return render_template('login.html')


@app.route('/view')
def View():
    return render_template('view.html')

@app.route('/home')
def home1():
    return render_template('home.html')

@app.route('/kyc_form')
def form():
    return render_template('kyc_form.html')


@app.route('/logout')


@app.route("/add", methods=["POST"])
def home():
    global cursor
    try:
        _name = request.form.get('username')
        _email = request.form.get('email')
        _salary = request.form.get('salary')
        _password = request.form.get('password')
        conn = mysql.connect()
        cursor = conn.cursor()
        stmt = "select * from employee where username=\"%s\""%(_name)
        sql1 = cursor.execute(stmt)
        sql1 = cursor.fetchone()
        if sql1 is None:
            sql = "INSERT INTO employee(username, email,salary,password) VALUES(%s, %s ,  %s , %s)"
            data = (_name, _email, _salary, _password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            data = (_name,_email,_salary)
            return render_template('employees.html', data=data)
        else:
            errorMessage = "Username is already exist"
            return render_template("login.html",error=errorMessage)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteEmployee', methods=['POST'])
def deleteEmployee():
    try:
        _id = request.form.get('id')
        print(_id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE id=%s", (_id))
        conn.commit()
        return render_template('view.html', datas=fetchListOfEmployees())
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def fetchListOfEmployees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/employeeUpdate', methods=['POST'])
def update_employee():
    try:
        _id = request.form.get('id')
        _name = request.form.get('username')
        _email = request.form.get('email')
        _salary = request.form.get('salary')
        _password = request.form.get('password')
        sql = "UPDATE employee SET username=%s, email=%s, salary=%s, password=%s WHERE id=%s"
        data = (_name, _email, _salary, _password, _id,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return render_template('view.html', datas=fetchListOfEmployees())
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/kyc_form', methods=['GET', 'POST'])
def kyc():
    global cursor
    if request.method=="POST":
        try:
            _name = request.form.get('name')
            _dob = request.form.get('dob')
            _id = request.form.get('ID')
            _email = request.form.get('email')
            _phone = request.form.get('phone')
            _aadhar=request.form.get('aadhar')
            _panno=request.form.get('panno')
            _address = request.form.get('address')
            _income = request.form.get('income')
            _emp_status = request.form.get('emp_status')
            _acc_type = request.form.get('acc_type')
            conn = mysql.connect()
            cursor = conn.cursor()
            stmt = "select * from users where name=\"%s\"" % (_name)
            sql1 = cursor.execute(stmt)
            sql1 = cursor.fetchone()
            if sql1 is None:
                stmt = "INSERT INTO users(name, dob,ID,email,phone,address,income,emp_status,acc_type,aadhar,panno) VALUES('{0}', '{1}', '{2}' , '{3}', '{4}', '{5}', '{6}', '{7}','{8}','{9}','{10}');".format(_name,_dob,_id, _email, _phone, _address, _income, _emp_status, _acc_type,_aadhar,_panno)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(stmt)
                conn.commit()
                status="Submitted Successfully."
                return render_template('kyc_form.html', status=status)
            else:
                errorMessage = "Name is already exist"
                return render_template("kyc_form.html", error=errorMessage)

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return render_template('kyc_form.html')

@app.route('/')
def get_emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # Execute a query to select user data
        cursor.execute("SELECT * FROM users")

        # Fetch all user records
        employees = cursor.fetchall()

        return employees
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
@app.route('/employeeList')
def employee_list():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")  # Replace 'employees' with your actual table name
        employees = cursor.fetchall()
        cursor.close()
        return render_template('employeelist.html', data=employees)
    except Exception as e:
        print(e)
        flash("An error occurred while fetching employee data.")
        return redirect(url_for('index'))  # Redirect to the homepage or an error page


# Define a route to display the form
@app.route('/')
def show_form():
    return render_template('kyc_form.html')

# Define a route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    global cursor
    try:
        name = request.form.get('name')
        dob = request.form.get('dob')
        national_id = request.form.get('ID')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        income = request.form.get('income')
        employment = request.form.get('emp_status')
        account_type = request.form.get('account_type')
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO users(name,dob,ID,email,phone,address,income,emp_status,account_type) VALUES(%s, %s , %s , %s, %s, %s, %s, %s, %s)"
        print(sql)
        data = (name, dob, national_id, email, phone, address, income, employment, account_type)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        data = (name, dob, national_id, email, phone, address, income, employment, account_type)
        return render_template('kyc_form.html', data=data)
            #return f"Form submitted successfully:<br>Name: {full_name}<br>Date of Birth: {dob}<br>National ID: {national_id}<br>Email: {email}<br>Phone: {phone}<br>Address: {address}<br>Income: {income}<br>Employment: {employment}<br>Account Type: {account_type}"
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

@app.route('/sendMail',methods=['GET', 'POST'])
def sendMail():
    if request.method=="POST":
        receiver_email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        email_address = "knowyourcustomer9@gmail.com"
        email_password = "bjdl gqpw jnta azjs"
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = receiver_email
        msg.set_content(message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        return render_template("sendMail.html",status="Email is successfully sent.")
    return render_template("sendMail.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
