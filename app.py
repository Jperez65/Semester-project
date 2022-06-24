from curses.ascii import US
from distutils.command.config import config
from flask import render_template
from flask import Flask
from flask_restful import reqparse, Api
from resources.config import Config
from resources.models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)  # create the api

############ Routes To Render Web Page ###########################
@app.route('/login')
def login_page(name=None):
    return render_template('login.html' )

@app.route('/landing')
def landing_page(name=None):
    return render_template('landing.html')

@app.route('/')
def registration_page(name=None):
    return render_template('registration_page.html')

################ Routes for API ####################################

@app.route('/api/register', methods=['POST'])
def register():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True, type=str,
                            help='first name field is required')
        # parser.add_argument('last_name', required=True, type=str,
        #                     help='email field is required')
        # parser.add_argument('email', required=True, type=str,
        #                     help='email field is required')
        # parser.add_argument('password', required=True, type=str,
        #                     help='password field is required')
        # parser.add_argument('phone_number', required=True, type=str,
        #                     help='phone number field is required')
        # parser.add_argument('g-recaptcha-response', required=True,
        #                     type=str, help='recaptcha response is missing')
        request_data = parser.parse_args(strict=True)
        print(request_data['first_name'])
        # User.create_user()
        response = '200'
    except Exception as e:
        print(e)
        response = '400'
    return response