import numpy as np
from keras._tf_keras.keras.models import Sequential, load_model
from keras._tf_keras.keras.layers import Dense, Dropout
from keras._tf_keras.keras import callbacks
from keras._tf_keras.keras.optimizers import Adam
import random
import json
import string

class HDAI:
    def __init__(self):
        self.preprocess_data()
        self.model = load_model('Assets/Databases/chatbot_model.h5')
    
    def Tokenizer(self, text):
        tokens = []
        token = ""
        for char in text:
            ## whitespace = ' \t\n\r\v\f'
            ## punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
            if char in string.whitespace or char in string.punctuation:
                if token:
                    tokens.append(token)
                    token = ""
                if char in string.punctuation:
                    tokens.append(char)
            if char in string.ascii_letters or char in string.digits:
                token += char
        if token:
            tokens.append(token)
        
        # convert to lower letters
        tokens = list(map(str.lower, tokens))
        
        return tokens
    
    def preprocess_data(self):
        # open the json file
        with open('Assets/Databases/NLP_Data.json', 'r') as json_data:
            self.data = json.load(json_data)
        # preprocess data
        self.words = []
        self.classes = []
        self.documents = []

        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                self.words.extend(self.Tokenizer(pattern))
                self.documents.append((self.Tokenizer(pattern), intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
    
    def make_bow(self, sentence, all_words, tkn_low=True):
        # use for prediction
        if tkn_low == True:
            sentence = str(sentence).lower()
            sentence_words = self.Tokenizer(sentence)
            bag = []
            for w in all_words:
                bag.append(1) if w in sentence_words else bag.append(0)
            return np.array(bag)
        # use for training
        if tkn_low == False:
            sentence_words = sentence
            bag = []
            for w in all_words:
                bag.append(1) if w in sentence_words else bag.append(0)
            return np.array(bag)
    
    def create_train_data(self):
        # create training data
        self.training = []
        output_empty = [0] * len(self.classes)


        for doc in self.documents:
            # Make Bow
            bag = self.make_bow(doc[0], self.words, False)

            # Make labels
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            
            self.training.append([bag, output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)

        # make train data
        self.train_x = np.array(list(self.training[:, 0]))
        self.train_y = np.array(list(self.training[:, 1]))
    
    def predict(self, sentence, model):
        p = self.make_bow(sentence, self.words, True)
        res = np.array(model.predict(np.array([p]))[0])
        ERROR_THRESHOLD = 0.5
        if np.max(res) > ERROR_THRESHOLD:
            result = {"intent": self.classes[list(res).index(np.max(res))], "probability": str(np.max(res))}
        else:
            result = False
        return result
    
    def get_response(self, intents_prd, all_intents):
        if intents_prd != False:
            tag = intents_prd['intent']
            list_of_intents = all_intents['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    responses = i['responses']
                    break
            return random.choice(responses)
        else:
            return "I'm sorry, I don't understand. Can you please rephrase your question?"
    
    def Chat(self, message):
        message = str(message).lower()
        ints = self.predict(message, self.model)
        res = str(self.get_response(ints, self.data))
        return res
    
    def Train(self):
        self.create_train_data()
        
        # create neural network
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.train_y[0]), activation='softmax'))

        # compile model
        adam = Adam(learning_rate=0.001)
        model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

        # fit model with callback
        early_stop = callbacks.EarlyStopping(monitor='loss', patience=35, restore_best_weights=True)
        hist = model.fit(self.train_x, self.train_y, epochs=200, batch_size=5, verbose=1, callbacks=[early_stop])

        # print best accuracy and loss that model achieved and callback saved it
        #print("Best accuracy: ", max(hist.history['accuracy']))
        #print("Best loss: ", min(hist.history['loss']))

        # save model
        model.save('Assets/Databases/chatbot_model.h5')

        #print("Model created")
        
        
n = HDAI()
#n.Train()

"""while True:
    m = str(input("TEXT ==>    ")).lower()
    if m == 'quit':
        break
    print(n.Chat(m))"""
