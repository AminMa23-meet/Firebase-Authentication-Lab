from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "sdjn;lakdfjase;oiasejf"

config = {
  "apiKey": "AIzaSyDzLPjVpYpO6NOWlOy_eeJEFp2murgRo2M",
  "authDomain": "hello-fba5c.firebaseapp.com",
  "projectId": "hello-fba5c",
  "storageBucket": "hello-fba5c.appspot.com",
  "messagingSenderId": "785823535127",
  "appId": "1:785823535127:web:623cf167fd83c52d2e8c52",
  "measurementId": "G-6S06XY5385",
  "databaseURL": "https://hello-fba5c-default-rtdb.europe-west1.firebasedatabase.app"
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
    return render_template("signup.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            user = {"email":email,"password":password,"name":name,"username":username,"bio":bio}
            print("hi")
            login_session['user']= auth.create_user_with_email_and_password(email, password)
            print("hi1")
            db.child('Users').child(login_session['user']["localId"]).set(user)
            print("hi2")
            return redirect(url_for('add_tweet'))
        except:
            print("Authentication error")
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    
    if request.method=='GET':
        return render_template("add_tweet.html")
    else:
        title = request.form['title']
        text = request.form['text']
    try:
        tweet = {"title":title,'text':text,"uid":login_session['user']["localId"]}
        db.child('Tweets').push(tweet)
        return redirect(url_for('all_tweets'))

    except:
        print('error')


        
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



@app.route('/all_tweets')
def all_tweets():
    t = db.child('Tweets').get().val().values()
    print(t)
    return render_template("tweets.html",tweets = t)



if __name__ == '__main__':
    app.run(debug=True)