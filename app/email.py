from flask_mail import Message
from flask import render_template
# from . import mail
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)

sender_email = 'joyluseno61@gmail.com'
subject_pref = 'Watchlist:'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'joyluseno61@gmail.com'
app.config['MAIL_PASSWORD'] = 'nessyjoy'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def mail_message(subject, template, to, **kwargs):
    email = Message(subject_pref + " " + subject,
                    sender=sender_email,
                    recipients=[to])
    email.body = render_template(template + ".txt", **kwargs)
    # email.html = render_template(template + ".html",**kwargs)
    # mail.send(email)
    print(email)


if __name__ == '__main__':
    app.run()
