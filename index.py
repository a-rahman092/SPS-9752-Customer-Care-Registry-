from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, random, smtplib, os, time, datetime
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = '12345'

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'REArTCNTTg'
app.config['MYSQL_PASSWORD'] = 'ZQOhm8hoc1'
app.config['MYSQL_DB'] = 'REArTCNTTg'

mysql = MySQL(app)

mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdulrahman209875@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rahman@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route('/')
def index():
   return render_template('index.html')



@app.route('/customerlogin', methods =['GET', 'POST'])
def customerlogin():
   msgdecline = ''
   if request.method == 'POST' and 'cemail' in request.form and 'cpassword' in request.form:
      cemail = request.form['cemail']
      cpassword = request.form['cpassword']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM customers_details WHERE customer_email = % s AND customer_password = % s', (cemail, cpassword, ))
      customers_details = cursor.fetchone()
      if customers_details:
         session['loggedin'] = True
         session['cemail'] = customers_details['customer_email']
         msgsuccess = 'Logged in successfully !'
         return redirect(url_for('welcome'))
      else:
         msgdecline = 'Incorrect Email / Password !'
   return render_template('customerlogin.html', msgdecline = msgdecline)



@app.route('/agentlogin', methods =['GET', 'POST'])
def agentlogin():
   msgdecline = ''
   if request.method == 'POST' and 'aemail' in request.form and 'apassword' in request.form:
      aemail = request.form['aemail']
      apassword = request.form['apassword']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM agent_information WHERE agent_email = % s AND agent_password = %s', (aemail, apassword,))
      agent_information = cursor.fetchone()
      if agent_information:
         session['loggedin'] = True
         session['aemail'] = agent_information['agent_email']
         msgsuccess = 'Logged in successfully !'
         return redirect(url_for('agentdashboard'))
      else:
         msgdecline = 'Incorrect Email / Password !'
   return render_template('agentlogin.html', msgdecline = msgdecline)



@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
   msgdecline = ''
   if request.method == 'POST' and 'adminusername' in request.form and 'adminpassword' in request.form:
      adminusername = request.form['adminusername']
      adminpassword = request.form['adminpassword']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM admin_details WHERE admin_username = % s AND admin_password = % s', (adminusername, adminpassword, ))
      admin = cursor.fetchone()
      if admin:
         session['loggedin'] = True
         session['adminusername'] = admin['admin_username']
         msgsuccess = 'Logged in successfully !'
         return redirect(url_for('admindashboard'))
      else:
         msgdecline = 'Incorrect Username / Password !'
   return render_template('adminlogin.html', msgdecline = msgdecline)
  
  
  
@app.route('/customerregister', methods =['GET', 'POST'])
def customerregister():
   msgdecline = ''
   if request.method == 'POST' and 'cname' in request.form and 'cemail' in request.form and 'cpassword' in request.form and 'cconfirmpassword' in request.form :
      cname = request.form['cname']
      cemail = request.form['cemail']
      cpassword = request.form['cpassword']
      cconfirmpassword = request.form['cconfirmpassword']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM customers_details WHERE customer_email = % s', (cemail, ))
      user_registration = cursor.fetchone()
      if user_registration:
         msgdecline = 'Account already exists ! Try Login'
      else:
         ts = time.time()
         timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         cursor.execute('INSERT INTO customers_details VALUES (%s, % s, % s, % s, % s)', (None, cname, cemail, cpassword, timestamp, ))
         mysql.connection.commit()
         msg = 'You have successfully registered !'
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello {},\nYou have successfully registered on Customer Care Registry".format(cname)
            mail.send(mailmsg)
         except:
            pass
         return redirect(url_for('customerlogin'))
   elif request.method == 'POST':
      msgdecline = 'Please fill out the form !'
   return render_template('customerregister.html', msgdecline = msgdecline)



@app.route('/agentregister', methods =['GET', 'POST'])
def agentregister():
   if not session.get("adminusername"):
      return redirect("/adminlogin")
   else:
      msgdecline = ''
      if request.method == 'POST' and 'aname' in request.form and 'aemail' in request.form and 'ausername' in request.form and 'apassword' in request.form and 'aconfirmpassword' in request.form :
         aname = request.form['aname']
         aemail = request.form['aemail']
         ausername = request.form['ausername']
         apassword = request.form['apassword']
         aconfirmpassword = request.form['aconfirmpassword']
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('SELECT * FROM agent_information WHERE agent_email = % s', (aemail, ))
         agent_information = cursor.fetchone()
         if agent_information:
            msgdecline = 'Account already exists ! Try Login'
         else:
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO agent_information VALUES (%s, % s, % s, % s, % s, % s)', (None, aname, aemail, ausername, apassword, timestamp,))
            mysql.connection.commit()
            msgsuccess = 'Agent Has been successfully registered !'
            try:
               mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
               mailmsg.body = "Hello Agent has been Successfully Registered"
               mail.send(mailmsg)
            except:
               pass
            return redirect(url_for('agentlogin'))
      elif request.method == 'POST':
         msg = 'Please fill out the form !'
   return render_template('agentregister.html', msgdecline = msgdecline)



@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
   if not session.get("cemail"):
      return redirect("/customerlogin")
   else:
      msgsuccess = ''
      msgdecline = ''
      cmail = session['cemail']
      mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      mycursor.execute('SELECT * FROM complaint_details WHERE customer_email = %s', (cmail,))
      data = mycursor.fetchall()
      if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'subject' in request.form and 'description' in request.form :
         name = request.form['name']
         email = request.form['email']
         subject = request.form['subject']
         description = request.form['description']
         ticketno = random.randint(100000, 999999)
         ts = time.time()
         timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('INSERT INTO complaint_details VALUES (%s, % s, % s, % s, % s, % s, % s, % s)', (ticketno, name, email, subject, description, timestamp ,"pending","pending", ))
         mysql.connection.commit()
         msgsuccess = 'Your complaint is successfully submitted !'
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello {},\nWe have received your complain\nYour Ticket Number: {}\nSubject: {}\nDescription: {}\n\nSoon you will be allotted an agent you will get allotment email".format(name, ticketno, subject, description)
            mail.send(mailmsg)
         except: 
            pass
      elif request.method == 'POST':
         msgdecline = 'Please fill out the form !'
   return render_template('welcome.html', msgsuccess = msgsuccess, data=data)
   


@app.route('/agentdashboard', methods =['GET', 'POST'])
def agentdashboard():
   if not session.get("aemail"):
      return redirect("/agentlogin")
   else:
      msg = ''
      aemail = session['aemail']
      mycursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      mycursor1.execute('SELECT agent_name FROM agent_information WHERE agent_email = %s', (aemail, ))
      agent = mycursor1.fetchone()
      
      for x in agent:
         agent_name = agent[x]
         
      mycursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      mycursor2.execute('SELECT * FROM complaint_details WHERE agent_name = %s', (agent_name, ))
      data = mycursor2.fetchall()
      if request.method == 'POST' and 'status' in request.form :
         status = request.form['status']
         ticketno = request.form['ticketno']
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('UPDATE complaint_details SET status = %s WHERE ticket_no = %s', (status, ticketno,) )
         mysql.connection.commit()
         msg = 'Your complaint is successfully solved !'
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello, \nYour complaint has been successfully solved\nYour Ticket Number: {}".format(ticketno)
            mail.send(mailmsg)
         except:
            pass
         return redirect(url_for('agentdashboard'))
      elif request.method == 'POST':
         msg = 'Please fill out the form !'
   return render_template('agentdashboard.html', msg = msg, data=data)



@app.route('/admindashboard', methods =['GET', 'POST'])
def admindashboard():
   if not session.get("adminusername"):
      return redirect("/adminlogin")
   else:
      msg = ''
      mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      mycursor.execute('SELECT * FROM complaint_details')
      data = mycursor.fetchall()
      mycursor.execute('SELECT * FROM agent_information')
      agent = mycursor.fetchall()
      if request.method == 'POST' and 'agentassign' in request.form :
         agentassign = request.form['agentassign']
         adminusername = request.form['adminusername']
         ticketno = request.form['ticketno']
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('UPDATE complaint_details SET agent_name = %s WHERE ticket_no = %s', (agentassign, ticketno,) )
         cursor.execute('UPDATE complaint_details SET status = %s WHERE ticket_no = %s', ("Agent Assigned", ticketno,) )
         mysql.connection.commit()
         msg = 'Your complaint is Assigned to Agent !'
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello,\nWe have received your complaint and agent {} has been Successfully Assigned\nYour Ticket Number: {}\n\nYou will be notified when your complain will be solved.".format(agentassign, ticketno)
            mail.send(mailmsg)
         except:
            pass
         return redirect(url_for('admindashboard'))
      elif request.method == 'POST':
         msg = 'Please fill out the form !'
   return render_template('admindashboard.html', msg = msg, data=data, agent=agent)



@app.route('/customerforgotpassword', methods =['GET', 'POST'])
def customerforgotpassword():
      msgdecline = ''
      if request.method == 'POST' and 'customerforgotemail' in request.form :
         forgotemail = request.form['customerforgotemail']
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('SELECT * FROM customers_details WHERE customer_email = % s', (forgotemail, ))
         customers_details = cursor.fetchone()
         if customers_details:
            session['customerforgotemail'] = forgotemail
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            try:
               mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
               mailmsg.body = "Hello, \nYour OTP is: {}\nCkick this link to reset your password".format(otp)
               mail.send(mailmsg)
            except:
               msgdecline = 'Oops! Something went wrong! Can\'t sent email'
            return redirect(url_for('enterotp'))
         else:
            msgdecline = 'This email is not registered!'
      return render_template('customerforgotpassword.html', msgdecline = msgdecline)
   
   
   
@app.route('/agentforgotpassword', methods =['GET', 'POST'])
def agentforgotpassword():
      msg = ''
      if request.method == 'POST' and 'agentforgotemail' in request.form :
         forgotemail = request.form['agentforgotemail']
         session['agentforgotemail'] = forgotemail
         otp = random.randint(1000, 9999)
         session['otp'] = otp
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello, \nYour OTP is: {}\nCkick this link to reset your password".format(otp)
            mail.send(mailmsg)
         except:
            msgdecline = 'Oops! Something went wrong! Can\'t sent email'
         return redirect(url_for('enterotp'))
      return render_template('agentforgotpassword.html', msg = msg)
   
   
   
@app.route('/adminforgotpassword', methods =['GET', 'POST'])
def adminforgotpassword():
      msg = ''
      if request.method == 'POST' and 'adminforgotemail' in request.form :
         forgotemail = request.form['adminforgotemail']
         session['adminforgotemail'] = forgotemail
         otp = random.randint(1000, 9999)
         session['otp'] = otp
         try:
            mailmsg = Message('Customer Care', sender = 'abdulrahman209875@gmail.com', recipients = ['abdulrahman92mohd@gmail.com'])
            mailmsg.body = "Hello, \nYour OTP is: {}\nCkick this link to reset your password".format(otp)
            mail.send(mailmsg)
         except:
            msgdecline = 'Oops! Something went wrong! Can\'t sent email'
         return redirect(url_for('enterotp'))
      return render_template('adminforgotpassword.html', msg = msg)
   


@app.route('/enterotp', methods =['GET', 'POST'])
def enterotp():
      msgdecline = ''
      if request.method == 'POST' and 'otp' in request.form :
         otp = int(request.form['otp'])
         if int(session['otp']) == otp:
            msgsuccess = 'success'
            return redirect(url_for('changepassword')) 
         else:
            msgdecline = 'You have entered wrong OTP'  
      elif request.method == 'POST':
         msg = 'Please fill out the form !'
      return render_template('enterotp.html', msgdecline = msgdecline)



@app.route('/changepassword', methods =['GET', 'POST'])
def changepassword():
      msgdecline = ''
      if request.method == 'POST' and 'newpassword' in request.form and 'confirmnewpassword' in request.form:
         newpassword = request.form['newpassword']
         confirmnewpassword = request.form['confirmnewpassword']
         if newpassword == confirmnewpassword:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if session.get("customerforgotemail"):
               cursor.execute('UPDATE customers_details SET customer_password = %s WHERE customer_email = %s', (newpassword, session['customerforgotemail'],) )
               mysql.connection.commit()
               msgsuccess = 'Your password changed !'
               return redirect(url_for('customerlogin'))
            elif session.get("agentforgotemail"):
               cursor.execute('UPDATE agent_information SET agent_password = %s WHERE agent_email = %s', (newpassword, session['agentforgotemail'],) )
               mysql.connection.commit()
               msgsuccess = 'Your password changed !'
               return redirect(url_for('agentlogin'))
            elif session.get("adminforgotemail"):
               cursor.execute('UPDATE admin_details SET admin_password = %s WHERE admin_email = %s', (newpassword, 'admin@xyz',) )
               mysql.connection.commit()
               msgsuccess = 'Your password changed !'
               return redirect(url_for('adminlogin'))
            else:
               msgdecline = 'Incorrect details'
         else:
            msgdecline = 'Incorrect details'    
      elif request.method == 'POST':
         msgdecline = 'Please fill out the form !'
      return render_template('changepassword.html', msgdecline = msgdecline)



@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('cemail', None)
   session.pop('aemail', None)
   session.pop('adminusername', None)
   return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True,port = 8080)
