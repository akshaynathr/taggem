from flask_mail import Mail,Message
from views import app
from views import session

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taggemin@gmail.com'
app.config['MAIL_PASSWORD'] = 'kl13a5812'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)


@app.route("/mailtest")
def index():
    msg = Message('Hello', sender = 'taggemin@gmail.com', recipients = ['akshaynathr@gmail.com'])
    msg.body = "This is the email body \n \n \n sent via TAGGEM " 
    mail.send(msg)
    return "Sent"



def send_mail(recepient,title,link,name):
    msg = Message(title, sender = 'taggemin@gmail.com', recipients = recepient)
    msg.body = name+" tagged you here:  "+link + "\n \n \n sent via TAGGEM "+"(http://www.taggem.in)"
    mail.send(msg)
    return "Sent"
