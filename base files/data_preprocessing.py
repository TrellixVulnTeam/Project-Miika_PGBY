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
