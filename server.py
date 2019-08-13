##################### START #####################################
from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from db import connectToMySQL
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

##################    READ INDEX  ###############################
@app.route("/")
def index():
    return render_template("index.html")

################# REGISTER HERE #################################
@app.route("/process1", methods=["POST"])
def add_newUser_to_db():
    is_valid = True		
    if len(request.form['fname']) < 1:
        is_valid = False
        flash("First name should be greater than 1", "ffm")
    if len(request.form['lname']) < 1:
        is_valid = False
        flash("Last name should be greater than 1", "flm")
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter again your email", "fem")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!", "fiem")
        is_valid = False
    if len(request.form['password']) < 2:
        is_valid = False
        flash("Please enter again your password", "fpm")
    if not is_valid:
        return redirect("/")
    else:
        # pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # print(pw_hash)
        mysql = connectToMySQL("loginreg_db")
        
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(email)s, %(password_hash)s)"
        data = {
            'fn': request.form['fname'],
            'ln': request.form['lname'],
            'email': request.form['email'],
            'password_hash': pw_hash
        }
        new_user_id = mysql.query_db(query, data)
        session['id']=new_user_id
        flash("Succesfully, signed up!", "success")
        return redirect("/show")

################ LOGIN HERE ####################################
@app.route("/process2", methods=["POST"])
def login():
    is_valid = True
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter again your email", "em")
    if len(request.form['password']) < 2:
        is_valid = False
        flash("Please enter again your password", "pm")
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL("loginreg_db")
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            'email': request.form['email'],
        }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                session['id']=result[0]['id']
                flash("Succesfully, signed in!", "success2")
            return redirect("/show")
        flash("You could not be logged in", "success3")
        return redirect('/')
        # session['email']=new_user_id


##################    SHOW   ##################################
@app.route("/show")
def show():
    mysql = connectToMySQL('loginreg_db')
    query = 'SELECT * FROM users WHERE id = %(id)s'
    data ={
        'id': session['id']
        # 'email': session['email']
    }
    users = mysql.query_db(query, data) 
    # print(users)
    return render_template("show.html", users = users )

################# END    #####################################
if __name__ == "__main__":
    app.run(debug=True)