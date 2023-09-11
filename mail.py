from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'btech.mshivam@gmail.com '
app.config['MAIL_PASSWORD'] = 'ajsshrnhcygyscch'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

@app.route('/')
def send_email():
    msg = Message('Hello', sender='btech.mshivam@gmail.com', recipients=['shivam@ulventech.com'])
    msg.body = 'This is a test email sent from Flask.'
    mail.send(msg)
    return 'Email sent successfully!'

if __name__ == '__main__':
    app.run()
