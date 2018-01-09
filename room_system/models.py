import json, urllib.request as re
from room_system import db
from datetime import datetime


# 天気API ダサいけどここに置く
def weather():
    citycode = '140010' #横浜
    resp = re.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    resp = json.loads(resp)
    return resp['forecasts'][0]['telop']


class StayMember(db.Model):
    __tablename__ = 'stay_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    enter_datetime = db.Column(db.DateTime, default=datetime.now())
    enter_weekday = db.Column(db.Integer, default=datetime.now().weekday())
    enter_weather = db.Column(db.Text, default=weather())

    def __repr__(self):
        return '<StayMember id={id} name={name!r} enter_datetime={enter_datetime} enter_weekday={enter_weekday} enter_weather={enter_weather}>'.format(id=self.id, name=self.name, enter_datetime=self.enter_datetime, enter_weekday=self.enter_weekday, enter_weather=self.enter_weather)

class LeftMember(db.Model):
    __tablename__ = 'left_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    enter_datetime = db.Column(db.DateTime, default=datetime.now())
    enter_weekday = db.Column(db.Integer, default=datetime.now().weekday())
    enter_weather = db.Column(db.Text, default=weather())
    exit_datetime = db.Column(db.DateTime, default=datetime.now())
    exit_weekday = db.Column(db.Integer, default=datetime.now().weekday())
    exit_weather = db.Column(db.Text, default=weather())

    def __repr__(self):
        return '<LeftMember id={id} name={name!r} enter_datetime={enter_datetime} enter_weekday={enter_weekday} enter_weather={enter_weather} exit_datetime={exit_datetime} exit_weekday={exit_weekday} exit_weather={exit_weather}>'.format(id=self.id, name=self.name, enter_datetime=self.enter_datetime, enter_weekday=self.enter_weekday, enter_weather=self.enter_weather, exit_datetime=self.exit_datetime, exit_weekday=self.exit_weekday, exit_weather=self.exit_weather)

def init():
    db.create_all()

def destroy():
    db.drop_all()

# タイムスタンプ要らないと思った
# 左辺という意味になってしまうらしい
# 天気は横浜
# 月曜が0
