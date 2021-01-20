import os
import sys
import subprocess
import pkg_resources

required = {'flask','flask-bootstrap','flask-mail','flask-wtf','wtforms','nltk',
            'pandas','speechrecognition','googletrans','rake-nltk','two-lists-similarity',
            'email-validator','pyaudio'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Installing the follwing required dependencies:",missing)
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


from flask import Flask, render_template, url_for, request, flash
from flask_bootstrap import Bootstrap
from forms import ContactForm
from flask_mail import Message, Mail
from text2image import speech_to_text, text_to_img

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
Bootstrap(app)

mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'autismai.contact@gmail.com'
app.config["MAIL_PASSWORD"] = 'vilncwbqtitdlweo'
app.config["SECRET_KEY"] = SECRET_KEY

mail.init_app(app)

@app.route("/")
def home():
    return render_template('home.html', title="Empowering Communications")

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/autismAI")
def autismAI():
    return render_template('autismAI.html', title="Product")

@app.route("/autismAI",methods=['POST','GET'])
def speak_anything():
    text_bn = speech_to_text()
    img_name = text_to_img(text_bn)
    return render_template('autismAI_result.html', image_name=img_name, converted_text=text_bn, title="Product")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if (request.method == 'POST'):
        if form.validate() == False:
          flash('All fields are required.')
          return render_template('contact.html', form=form)
        else:
          msg = Message(form.subject.data, sender=form.email.data, recipients=['autismai.contact@gmail.com'])
          msg.body = """
          From: %s [%s]
          %s
          """ % (form.name.data, form.email.data, form.message.data)
          mail.send(msg)

          return render_template('contact.html', success=True)

    elif (request.method == 'GET'):
        return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
