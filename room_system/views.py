from flask import request, jsonify, render_template, redirect, flash, url_for
from room_system import app 
from room_system.models import StayMember, LeftMember, checkOut
from room_system.function import faceChecker

@app.route('/')
def index():
    stay_members = StayMember.getIndex()
    left_members = LeftMember.getIndex()
    return render_template('index.html', stay_members=stay_members, left_members=left_members)

@app.route('/enter', methods=['POST'])
def enter():
    upload_file = request.files['enter_face']
    member = faceChecker(upload_file)
    if (not StayMember.already(member)):
        flash(StayMember.checkIn(member))
    return redirect(url_for('index'))

@app.route('/exit', methods=['POST'])
def exit():
    upload_file = request.files['exit_face']
    member = faceChecker(upload_file)
    if (StayMember.already(member)):
        flash(checkOut(member))
    return redirect(url_for('index'))

@app.route('/search')
def search():
    app.config['JSON_AS_ASCII'] = False
    response = []
    query = request.args['query']
    if (query == 'now'):
        result = StayMember.getIndex() 
    elif (query == 'today'):
        result = LeftMember.today() 
    else:
        result = None
    for i in result:
        response.append(i.name)
    return jsonify(response)
