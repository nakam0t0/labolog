import numpy as np
from PIL import Image
from room_system import db
from room_system.models import StayMember, LeftMember 
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

def stayIndex():
    return StayMember.query.order_by(StayMember.id.desc()).all()

def leftIndex():
    return LeftMember.query.order_by(LeftMember.id.desc()).all()


def alreadyStay(name):
    from room_system.models import StayMember
    result = StayMember.query.filter(StayMember.name == name).first()
    return (result is not None)

def checkIn(name):
    from room_system.models import StayMember
    member = StayMember(name=name)
    db.session.add(member)
    db.session.commit()
    return 'こんにちは' + name + 'さん' 

def checkOut(name):
    stay_log = StayMember.query.filter(StayMember.name == name).first()
    en_dt = stay_log.enter_datetime
    en_wd = stay_log.enter_weekday
    en_wt = stay_log.enter_weather
    member = LeftMember(name=name, enter_datetime=en_dt, enter_weekday=en_wd, enter_weather=en_wd)
    db.session.add(member)
    db.session.commit()
    db.session.delete(stay_log)
    db.session.commit()
    return 'さようなら' + name + 'さん' 

# モデルを構築
def build_model(in_shape, nb_classes):
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, 
	border_mode='same',
	input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, 3, 3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten()) 
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy',
	optimizer='rmsprop',
	metrics=['accuracy'])
    return model

def faceChecker(fname):
    image_size = 50
    categories = ['中本　昌吾', '誰か']
    nb_classes = len(categories)
    answer = ''

    # 入力画像をNumpyに変換
    X = []
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    in_data = np.asarray(img)
    X.append(in_data)
    X = np.array(X)

    # CNNのモデルを構築
    model = build_model(X.shape[1:], nb_classes)
    model.load_weights("./room_system/face-model.hdf5")

    # データを予測
    pre = model.predict(X)
    for i, p in enumerate(pre):
        y = p.argmax()
        answer = categories[y]
    return answer
