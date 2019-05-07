from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir), autoescape=True)

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

signup = """
<!DOCTYPE html>
<html lang="en">
  <head>

    <title>SignUp</title>
    <link rel="stylesheet" href="static/app.css" />
  </head>
  <body>
    <form action="/usersignup" id="form" method="POST">
        <h1>Register</h1>
        <label for="username">Username</label>
        <input type="text" name="username" id="username" value="{0}" required/>
        <p style="color: red">{1}</p>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" value="{2}" required />
        <p style="color: red">{3}</p>
    
        <label for="password">Re-enter your password</label>
        <input type="password" name="password2" id="password2" value="{4}" required />
        <p style="color: red">{5}</p>
        <label for="email">Email</label>
        <input type="text" name="email" id="email" value="{6}" />
        <p style="color: red">{7}</p>
    
        <button type="submit">Register</button>
  </form>
 </body>
</html>
"""


@app.route("/")
def index():
    print("Index page!")
    template = jinja_env.get_template('signup_form.html')
    return template.render()
    
# a registration form

@app.route("/usersignup")
def display_form():
    return render_template('signup_form.html')


@app.route("/usersignup", methods=['POST'])



def register():
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    password2 = cgi.escape(request.form['password2'])
    email = cgi.escape(request.form['email'])



    usernameError =""
    passwordError = ""
    password2Error =""
    emailError = ""
    
    #VALIDATIONS
    
    #username validations
    if " " in username:
        usernameError = "username cannot contain a space"
    if len(username) < 3 or len(username) > 20:
        usernameError = "username must be between 3 and 20 characters"
    #password validations    
    if not password:
        passwordError = "Password is required"
    elif len(password) < 3 or len(password) > 20:
        passwordError = "Password must be between 3 and 20 characters"
    else:
        hasNumber = False
        for char in password:
            if char.isdigit():
                hasNumber = True
        if not hasNumber:
            passwordError = "Password must contain a number"
    if password  != password2:
        password2Error = "Password does not match"
    #email validations
    if len(email) > 0:
        if " " in email:
            emailError = "Email cannot contain a space"
        if len(email) < 6 or len(email) > 40:
            emailError = "Email must be between 6 and 40 characters"
        if "@" not in email:
            emailError = "Email must contain @ symbol"
        if email.count("@") > 1:
            emailError = "Email can only have one @ symbol"
        if "." not in email:
            emailError = "Email must contain period"
        if email.count(".") > 1:
            emailError = "Email can only have one period"
    

    if usernameError or passwordError or password2Error or emailError:
        print("there was an error!")
        password = "" #Gotta retype that password, fam
        password2 = "" #Gotta retype that password, fam
        email = "" #Gotta retype that email too, doe
        content = signup.format(username, usernameError, 
        password, passwordError, password2, password2Error, email, emailError)
        return content
    #else return the successful redirect below    
    return redirect('/welcome?username={0}'.format(username))
    






@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)


app.run()
