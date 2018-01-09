import os
from flask import request, jsonify, render_template
from room_system import app 
from room_system.function import faceChecker, checkIn, checkOut, alreadyStay, stayIndex, leftIndex, leftToday 


@app.route('/')
def index():
    stay_members = stayIndex()
    left_members = leftIndex()
    return render_template('index.html', stay_members=stay_members, left_members=left_members)

@app.route('/enter', methods=['POST'])
def enter():
    upload_file = request.files['enter_face']
    member = faceChecker(upload_file)
    if (not alreadyStay(member)):
        return checkIn(member)
    else:
        return ''
        

@app.route('/exit', methods=['POST'])
def exit():
    upload_file = request.files['exit_face']
    member = faceChecker(upload_file)
    if (alreadyStay(member)):
        return checkOut(member)
    else:
        return ''

@app.route('/search')
def search():
    app.config['JSON_AS_ASCII'] = False
    response = []
    query = request.args['query']
    if (query == 'now'):
        result = stayIndex() 
    elif (query == 'today'):
        result = leftToday() 
    else:
        result = None
    for i in result:
        response.append(i.name)
    return jsonify(response)
