from flask import Blueprint, jsonify, request,make_response
import hashlib
import binascii
import os
import json
import collections
import pyodbc
import requests
from datetime import datetime
user_bp = Blueprint('user', __name__)

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
print('Database connection sucessfully')


@user_bp.route('/register/', methods=["POST"])
def Register():
    cursor = conn.cursor()
    cursor.execute("select Email from User_Details where Email='"+request.json["email"]+"'")
    emailRows = cursor.fetchall()
    if len(emailRows) == 0:
        name = request.json["name"]
        passwordHash = request.json["password"].encode()
        passwordSalt = request.json["password"].encode()
        email = request.json["email"]
        status = request.json["status"]
        gender = request.json["gender"]
        useCreated = datetime.now()
        userModified = datetime.now()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO User_Details(Name,PasswordHash,PasswordSalt,Email,Status,Gender,User_Created_Timestamp,User_Modified_Timestamp) VALUES (?,?,?,?,?,?,?,?)',
                    (name, bytes(passwordHash), bytes(passwordSalt), email, status, gender, useCreated, userModified))
        conn.commit()

        return jsonify({'statusCode':'201', 'message' : "User created successfully. , Success! " })
    else:
        return jsonify({'statusCode':'500', 'message' : "Email Id Already Exist! " })
        return make_response('Email Id Already Exist!')    


@user_bp.route('/register/', methods=["GET"])
def Get():
    data = []
    cursor = conn.cursor()
    cursor.execute("select UserId,Name,Email,Status,Gender from User_Details")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'empId': row[0], 'name': row[1], 'email': row[2], 'status': row[3], 'gender': row[4]})
    #return jsonify(data)
    return jsonify({'statusCode':'201','message':'success','result':data})

@user_bp.route('/register/', methods=["PUT"])
def Put():
    userid= request.json["empId"]
    name = request.json["name"]
    if request.json["password"] != "------":
        passwordHash = request.json["password"].encode()
        passwordSalt = request.json["password"].encode()
    email = request.json["email"]
    status = request.json["status"]
    gender = request.json["gender"]
    useCreated = datetime.now()
    userModified = datetime.now()
    cursor = conn.cursor()
    if request.json["password"] != "------":
        cursor.execute("UPDATE User_Details SET Name = ?, PasswordHash = ?,PasswordSalt = ?,Email = ?, Status = ?,Gender = ?,User_Created_Timestamp = ?,User_Modified_Timestamp = ?  WHERE UserId = ?", name, bytes(passwordHash),bytes(passwordSalt),email,status,gender,useCreated,userModified,userid)
    else:
        cursor.execute("UPDATE User_Details SET Name = ?,Email = ?, Status = ?,Gender = ?,User_Created_Timestamp = ?,User_Modified_Timestamp = ?  WHERE UserId = ?", name,email,status,gender,useCreated,userModified,userid)
    conn.commit()
    return jsonify({'statusCode':'201', 'message' : "User updated successfully. , Success! " })

