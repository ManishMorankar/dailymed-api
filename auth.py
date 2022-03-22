from flask import Flask, jsonify, request, make_response,Blueprint
import jwt 
import datetime
import pyodbc
from functools import wraps
auth_bp = Blueprint('auth', __name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

def dbconn():
    global conn
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=10.10.20.109;"
        "Database=DailyMedDB_Live;"
        "UID=sa;"
        "PWD=Admin!@#20;"
        # "Trusted_Connection=yes;"
    )

dbconn()
# print('Database connection sucessfully')
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 403
#         try: 
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 403

#         return f(*args, **kwargs)

#     return decorated

# @auth_bp.route('/unprotected')
# def unprotected():
#     return jsonify({'message' : 'Anyone can view this!'})

# @auth_bp.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message' : 'This is only available for people with valid tokens.'})

@auth_bp.route('/login', methods=["POST"])
def login():
    passwordHash = request.json["password"].encode()
    email = request.json["email"]
    data = []
    cursor = conn.cursor()
    cursor.execute("select * from User_Details where Email='"+email+"'")
    rows = cursor.fetchall()

    for row in rows:
        UserResult={'userName':row[1],'empId':row[0],'email':row[4]}
        if  email == row[4] and passwordHash == row[2]:
            token = jwt.encode({'user' : email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=600)}, app.config['SECRET_KEY'])
            cursor = conn.cursor()
            cursor.execute("UPDATE User_Details SET Token = ?, LoginDate = ? WHERE Email = ?", token, datetime.datetime.now() ,email)
            conn.commit()
            # return jsonify({'token' : token.decode('UTF-8')})
            return jsonify({'statusCode':'200','message':'Login Successfully ','result':{'token':token,'user':UserResult}})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@auth_bp.route('/logout', methods=["POST"])
def logout():
    email = request.json["email"]
    cursor = conn.cursor()
    cursor.execute("select Token from User_Details where Email='"+email+"'")
    rows = cursor.fetchall()

    for row in rows:
        cursor = conn.cursor()
        token = None
        cursor.execute("UPDATE User_Details SET Token = ?, RequestTime = ? WHERE Email = ?", token, datetime.datetime.now() ,email)
        conn.commit()
        return jsonify({'statusCode':'200'})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})    

# if __name__ == '__main__':
#     app.run(debug=True)