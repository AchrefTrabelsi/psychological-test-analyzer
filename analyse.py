from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np
import pickle

class analyse():
    def __init__(self):

        self.trunc_type='post'
        self.padding_type='post'
        self.oov_tok = "<OOV>"
        self.max_length = 100
        self.class_names = ['Negative', 'Positive']
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.model=load_model("model_multiple_bidi_lstm_.h5")
    def analyser(self,text):
        sentence=[]
        sentence.append(text)
        sentence.append('')
        sequences = self.tokenizer.texts_to_sequences(sentence)
        padded = pad_sequences(sequences,maxlen=self.max_length, padding=self.padding_type, 
                            truncating=self.trunc_type)
        in_f=np.array(padded)
        predictions=self.model.predict(in_f)
        return predictions[0][0]