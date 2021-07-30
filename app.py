from flask import Flask, render_template
from flask_socketio import SocketIO
#import tensorflow as tf
#from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
#from keras.preprocessing.text import Tokenizer
#import tensorflow.compat.v1 as tf
#from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from joblib import dump, load
from utils import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
#tf.disable_v2_behavior()

@app.route('/', methods=['GET', 'POST'])
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    mess = str(json)
    print('received my event: ' + mess)
    print(type(json))
    print(json.keys())
    
    '''
    model = load_model('/Volumes/DATA/UNIMI/Text Mining and Sentiment Analysis/hate_speech_detection/lstm')
    tokenizer = Tokenizer()
    text = pd.Series(json['message'])
    text_tokenize = tokenizer.texts_to_sequences(text)
    label_pred = model.predict_classes(pad_sequences(text_tokenize, maxlen=120))
    print("label: " + str(label_pred[0]))
    #socketio.emit('my response', json, callback=messageReceived)
    '''
    
    #gbdt = load('/Volumes/DATA/UNIMI/Text Mining and Sentiment Analysis/hate_speech_detection/best_gbdt.pkl')
    model = load('/Volumes/DATA/UNIMI/Text Mining and Sentiment Analysis/hate_speech_detection/gbdt.pkl')
    #json['message'] = "not allowed"
    #socketio.emit('my response', json, callback=messageReceived)
    
    label_pred = model.predict(pd.Series(json['message']))
    
    if label_pred[0] == 1:
        json['message'] = "Hate speech dectected"
        socketio.emit('my response', json, callback=messageReceived)
    elif label_pred[0] == 2:
        json['message'] = "Hate speech dectected"
        socketio.emit('my response', json, callback=messageReceived)
    else:
        socketio.emit('my response', json, callback=messageReceived)
    


if __name__ == '__main__':
    socketio.run(app, debug=True) 