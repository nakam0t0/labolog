import json, urllib.request as re
from room_system import db
from datetime import datetime

# 曜日変換
def weekday():
    if datetime.now().weekday() == 0:
        return '月'
    if datetime.now().weekday() == 1:
        return '火'
    if datetime.now().weekday() == 2:
        return '水'
    if datetime.now().weekday() == 3:
        return '木'
    if datetime.now().weekday() == 4:
        return '金'
    if datetime.now().weekday() == 5:
        return '土'
    return '日'

# 天気API
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
    enter_weekday = db.Column(db.Integer, default=weekday())
    enter_weather = db.Column(db.Text, default=weather())

    @classmethod
    def getIndex(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def already(cls, name):
        result = cls.query.filter(cls.name == name).first()
        return (result is not None)

    @classmethod
    def checkIn(cls, name):
        member = cls(name=name)
        db.session.add(member)
        db.session.commit()
        return 'こんにちは' + name + 'さん' 

    def __repr__(self):
        return '<StayMember id={id} name={name!r} enter_datetime={enter_datetime} enter_weekday={enter_weekday} enter_weather={enter_weather}>'.format(id=self.id, name=self.name, enter_datetime=self.enter_datetime, enter_weekday=self.enter_weekday, enter_weather=self.enter_weather)

class LeftMember(db.Model):
    __tablename__ = 'left_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    enter_datetime = db.Column(db.DateTime, default=datetime.now())
    enter_weekday = db.Column(db.Integer, default=weekday())
    enter_weather = db.Column(db.Text, default=weather())
    exit_datetime = db.Column(db.DateTime, default=datetime.now())
    exit_weekday = db.Column(db.Integer, default=weekday())
    exit_weather = db.Column(db.Text, default=weather())
    
    @classmethod
    def getIndex(cls):
        return cls.query.order_by(cls.id.desc()).all()
    
    @classmethod
    def today(cls):
        today = datetime.date.today()
        return cls.query.filter(cls.exit_datetime >= today).all()

    def __repr__(self):
        return '<LeftMember id={id} name={name!r} enter_datetime={enter_datetime} enter_weekday={enter_weekday} enter_weather={enter_weather} exit_datetime={exit_datetime} exit_weekday={exit_weekday} exit_weather={exit_weather}>'.format(id=self.id, name=self.name, enter_datetime=self.enter_datetime, enter_weekday=self.enter_weekday, enter_weather=self.enter_weather, exit_datetime=self.exit_datetime, exit_weekday=self.exit_weekday, exit_weather=self.exit_weather)

def checkOut(name):
    stay_log = StayMember.query.filter(StayMember.name == name).first()
    en_dt = stay_log.enter_datetime
    en_wd = stay_log.enter_weekday
    en_wt = stay_log.enter_weather
    member = LeftMember(name=name, enter_datetime=en_dt, enter_weekday=en_wd, enter_weather=en_wt)
    db.session.add(member)
    db.session.commit()
    db.session.delete(stay_log)
    db.session.commit()
    return 'さようなら' + name + 'さん' 

def init():
    db.create_all()

def destroy():
    db.drop_all()

# タイムスタンプ要らないと思った
# 左辺という意味になってしまうらしい
# 天気は横浜
# 月曜が0
