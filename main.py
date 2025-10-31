from flask import *
from flask_mail import *
from random import *
app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIN_PORT"] = 465
app.config["MAIL_USERNAME"] = "codingaltestemail.com"
app.config["MAIL_PASSWORD"] = 'ojoukrigdwnofixq'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail= Mail(app)
otp=randint(000000,999999)
@app.route('/verify',methods=["POST"])
def verify():
    email=request.form["email"]
    msg = Message('OTP',sender="codingaltestemail@gmail.com",recipiants=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template('page.html')
@app.route('/validate',methods=["POST"])
def validate():
    user_otp=request.form["otp"]
    if otp == int(user_otp):
        return"<h3>Verification was successful.You may proceed</h3>"
    else:
        return"<h3>Verification failed.Wrong OTP🥀</h3>"
@app.route('/')
def index():
    return render_template('index.html')
app.run(host='0.0.0.0', port=8080, debug=True)