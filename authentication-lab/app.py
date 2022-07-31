from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config[https://console.firebase.google.com/project/hello-fba5c/database/hello-fba5c-default-rtdb/data/~2F'SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDzLPjVpYpO6NOWlOy_eeJEFp2murgRo2M",
  "authDomain": "hello-fba5c.firebaseapp.com",
  "projectId": "hello-fba5c",
  "storageBucket": "hello-fba5c.appspot.com",
  "messagingSenderId": "785823535127",
  "appId": "1:785823535127:web:623cf167fd83c52d2e8c52",
  "measurementId": "G-6S06XY5385",
  "databaseURL": "https://console.firebase.google.com/project/hello-fba5c/database/hello-fba5c-default-rtdb/data/~2F"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))  
        except:
            error = "Authentication error"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('signin'))
        except:
            error = "Authentication error"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

    



if __name__ == '__main__':
    app.run(debug=True)