from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lbs14903;PWD=1N4walQ5ywwiwP7c;",'','')

@app.route('/')
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'passwords' in request.form and 'cpassword' in request.form :
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        passwords = request.form['passwords']
        cpassword = request.form['cpassword']
        stmt = ibm_db.prepare(conn,'SELECT * FROM appuser WHERE username = ?')
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not passwords or not email:
            msg = 'Please fill out the form !'
        else:
            prep_stmt = ibm_db.prepare(conn,"INSERT INTO appuser VALUES(?, ?, ?, ?, ?, ?)")
            ibm_db.bind_param(prep_stmt, 1, fullname)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, phonenumber)
            ibm_db.bind_param(prep_stmt, 5, passwords)
            ibm_db.bind_param(prep_stmt, 6, cpassword)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg = msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)
