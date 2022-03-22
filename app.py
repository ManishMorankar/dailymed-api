from flask import Flask
from flask import request
from home import home_bp
from auth import auth_bp
from user import user_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp,url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)