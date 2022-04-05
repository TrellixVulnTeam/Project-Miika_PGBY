### DATA PROCESSING

# Importing libraries
import re

# Reading text files into variables
lines = open('dataset/lines.txt', encoding='utf-8',
             errors='ignore').read().split('\n')

conversation = open('dataset/conversations.txt', encoding='utf-8',
                    errors='ignore').read().split('\n')

# Extracting the required data from dataset
convoFlow = []
for convo in conversation:
    convoFlow.append(convo.split(' +++$+++ ')[-1][1:-1].replace("'", " ").replace(",", "").split())

dialogs = {}
for line in lines:
    dialogs[line.split(' +++$+++ ')[0]] = line.split(' +++$+++ ')[-1]

## delete
del (lines, conversation)

# Mapping Answers to Questions
questions = []
answers = []

# Convo Replies(Answers) get mapped to Convos(Questions)
for convo in convoFlow:
    for i in range(len(convo) - 1):
        questions.append(dialogs[convo[i]])
        answers.append(dialogs[convo[i + 1]])

## delete
del (dialogs, convoFlow)

#        max_len = 13         #
# Sorting dialogs based on length.
sortedQues = []
sortedAns = []
for i in range(len(questions)):
    if len(questions[i]) < 13:
        sortedQues.append(questions[i])
        sortedAns.append(answers[i])

# Formatting all punctuations
def formatText(txt):
    txt = txt.lower()
    txt = re.sub(r"i'm", "i am", txt)
    txt = re.sub(r"he's", "he is", txt)
    txt = re.sub(r"she's", "she is", txt)
    txt = re.sub(r"that's", "that is", txt)
    txt = re.sub(r"what's", "what is", txt)
    txt = re.sub(r"where's", "where is", txt)
    txt = re.sub(r"\'ll", " will", txt)
    txt = re.sub(r"\'ve", " have", txt)
    txt = re.sub(r"\'re", " are", txt)
    txt = re.sub(r"\'d", " would", txt)
    txt = re.sub(r"won't", "will not", txt)
    txt = re.sub(r"can't", "can not", txt)
    txt = re.sub(r"[^\w\s]", "", txt)
    return txt

# Appending the formatted text
formattedQues = []
formattedAns = []

for line in sortedQues:
    formattedQues.append(formatText(line))

for line in sortedAns:
    formattedAns.append(formatText(line))

## delete
del (answers, questions)

for i in range(len(formattedAns)):
    formattedAns[i] = ' '.join(formattedAns[i].split()[:11])

del (sortedAns, sortedQues)

# Limiting dataset to 30000 values
formattedAns = formattedAns[:30000]
formattedQues = formattedQues[:30000]
## delete


# Removing similar sentences
word2count = {}

for line in formattedQues:
    for word in line.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
for line in formattedAns:
    for word in line.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1


# Removing words with less than 5 word count
threshold = 5

vocab = {}
word_num = 0
for word, count in word2count.items():
    if count >= threshold:
        vocab[word] = word_num
        word_num += 1

## delete
del (word2count, threshold)
del word_num

# Adding tokens to classify text
for i in range(len(formattedAns)):
    formattedAns[i] = '<SOS> ' + formattedAns[i] + ' <EOS>'

tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
x = len(vocab)
for token in tokens:
    vocab[token] = x
    x += 1

# Replacing dataset names with variables
vocab['cameron'] = vocab['<PAD>']
vocab['<PAD>'] = 0

## delete
del tokens
del x

# Inversing Vocabulary
inv_vocab = {w: v for v, w in vocab.items()}

## delete
del i

# Input for passing text to Calculate Output
encoderInput = []
for line in formattedQues:
    tempList = []
    for word in line.split():
        if word not in vocab:
            tempList.append(vocab['<OUT>'])
        else:
            tempList.append(vocab[word])

    encoderInput.append(tempList)

decoderInput = []
for line in formattedAns:
    tempList = []
    for word in line.split():
        if word not in vocab:
            tempList.append(vocab['<OUT>'])
        else:
            tempList.append(vocab[word])
    decoderInput.append(tempList)

### delete
del (formattedAns, formattedQues)

from tensorflow.keras.preprocessing.sequence import pad_sequences

encoderInput = pad_sequences(encoderInput, 13, padding='post', truncating='post')
decoderInput = pad_sequences(decoderInput, 13, padding='post', truncating='post')

decoder_final_output = []
for i in decoderInput:
    decoder_final_output.append(i[1:])

decoder_final_output = pad_sequences(decoder_final_output, 13, padding='post', truncating='post')

del i

from tensorflow.keras.utils import to_categorical

decoder_final_output = to_categorical(decoder_final_output, len(vocab))

### ML MODEL

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input

enc_inp = Input(shape=(13,))
dec_inp = Input(shape=(13,))

VOCAB_SIZE = len(vocab)
embed = Embedding(VOCAB_SIZE + 1, output_dim=50,
                  input_length=13,
                  trainable=True
                  )

enc_embed = embed(enc_inp)
enc_lstm = LSTM(400, return_sequences=True, return_state=True)
enc_op, h, c = enc_lstm(enc_embed)
enc_states = [h, c]

dec_embed = embed(dec_inp)
dec_lstm = LSTM(400, return_sequences=True, return_state=True)
dec_op, _, _ = dec_lstm(dec_embed, initial_state=enc_states)

dense = Dense(VOCAB_SIZE, activation='softmax')

dense_op = dense(dec_op)

model = Model([enc_inp, dec_inp], dense_op)

model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer='adam')

model.fit([encoderInput, decoderInput], decoder_final_output, epochs=40)

model.save('miika_model.h5')

### INFERENCE

import numpy as np
from keras.models import load_model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input

model = load_model('miika_model.h5')
enc_model = Model([enc_inp], enc_states)

# decoder Model
decoder_state_input_h = Input(shape=(400,))
decoder_state_input_c = Input(shape=(400,))

decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_outputs, state_h, state_c = dec_lstm(dec_embed,
                                             initial_state=decoder_states_inputs)

decoder_states = [state_h, state_c]

dec_model = Model([dec_inp] + decoder_states_inputs,
                  [decoder_outputs] + decoder_states)

from keras.preprocessing.sequence import pad_sequences

print("##########################################")
print("#              Project Miika             #")
print("##########################################")

prepro1 = ""
while prepro1 != 'q':
    prepro1 = input("You : ")
    ## prepro1 = "Hello"

    prepro1 = formatText(prepro1)
    ## prepro1 = "hello"

    prepro = [prepro1]
    ## prepro1 = ["hello"]

    txt = []
    for x in prepro:
        # x = "hello"
        tempList = []
        for y in x.split():
            ## y = "hello"
            try:
                tempList.append(vocab[y])
                ## vocab['hello'] = 454
            except:
                tempList.append(vocab['<OUT>'])
        txt.append(tempList)

    ## txt = [[454]]
    txt = pad_sequences(txt, 13, padding='post')

    ## txt = [[454,0,0,0,.........13]]

    stat = enc_model.predict(txt)

    empty_target_seq = np.zeros((1, 1))
    ##   empty_target_seq = [0]

    empty_target_seq[0, 0] = vocab['<SOS>']
    ##    empty_target_seq = [255]

    stop_condition = False
    decoded_translation = ''

    while not stop_condition:

        dec_outputs, h, c = dec_model.predict([empty_target_seq] + stat)
        decoder_concat_input = dense(dec_outputs)
        ## decoder_concat_input = [0.1, 0.2, .4, .0, ...............]

        sampled_word_index = np.argmax(decoder_concat_input[0, -1, :])
        ## sampled_word_index = [2]

        sampled_word = inv_vocab[sampled_word_index] + ' '

        ## inv_vocab[2] = 'hi'
        ## sampled_word = 'hi '

        if sampled_word != '<EOS> ':
            decoded_translation += sampled_word

        if sampled_word == '<EOS> ' or len(decoded_translation.split()) > 13:
            stop_condition = True

        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        ## <SOS> - > hi
        ## hi --> <EOS>
        stat = [h, c]

    print("Miika : ", decoded_translation)
    print("==============================================")
