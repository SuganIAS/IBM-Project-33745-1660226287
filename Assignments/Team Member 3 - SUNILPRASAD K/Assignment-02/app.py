from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ztc89378;PWD=HSYKGIqGBcRZVRHK",'','')
print("Connected Successfully !")

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/about")
def aboutpage():
    return render_template('about.html')

@app.route("/login", methods =['POST','GET'])
def loginpage():
    smsg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if((email and password) ):
            sql = "SELECT * FROM signup WHERE email = 'email'"
            stmt = ibm_db.exec_immediate(conn, sql)

            if(ibm_db.fetch_row(stmt)):
                row = ibm_db.fetch_both(stmt)

                if(row['email'] == email and row['password'] == password):
                    session['email'] = row['email']
                    session['pass'] = row['pass']
                    smsg = 'Logged in successfully !'
                    return render_template('about.html', smsg = smsg)
                else:
                    smsg = 'Incorrect username / password !'
                    return render_template('signin.html', smsg = smsg)
            else:
                smsg = 'Not yet registered'
                return render_template('signup.html', smsg = smsg)
        else:
                smsg = 'Fill all the details'
                return render_template('signin.html', smsg = smsg)
    else:
        return render_template('home.html')
            
            

@app.route("/signin")
def signinpage():
    return render_template('signin.html')

                    



        #sql = "SELECT * FROM signup WHERE email =?"
        #stmt = ibm_db.prepare(conn, sql)
        #ibm_db.bind_param(stmt,1,email)
        #ibm_db.execute(stmt)
        #account = ibm_db.fetch_assoc(stmt)

        #stmt = 'SELECT * FROM signup WHERE email = % s AND password = % s', (email, password, )
        #cur = ibm_db.prepare(conn, stmt)
        #ibm_db.exec_immediate(cur)
        #account = ibm_db.fetch_assoc(cur)

        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM signup WHERE email = % s AND password = % s', (email, password, ))
        #account = cursor.fetchone()
        #if account:
            #session['loggedin'] = True
            #session['id'] = account['id']
            #session['email'] = account['email']
            #msg = 'Logged in successfully !'
            #return render_template('about.html', smsg = smsg)
        #else:
            #msg = 'Incorrect username / password !'
    #return render_template('signin.html', smsg = smsg)

@app.route("/signup")
def signuppage():
    return render_template('signup.html')

@app.route("/signinrec",methods = ['POST', 'GET'])
def signinrec():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM signup WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signin.html', msg="You are already a member, please signin using your details")
        else:
            insert_sql = "INSERT INTO signup VALUES (?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.execute(prep_stmt)
    
        return render_template('home.html', msg="registered successfuly..")

    

    
