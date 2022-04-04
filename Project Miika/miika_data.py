# Importing libraries
import re


# Reading text files into variables
lines = open('dataset/lines.txt', encoding='utf-8', errors = 'ignore').read().split('\n')
conversation = open('dataset/conversations.txt', encoding='utf-8', errors = 'ignore').read().split('\n')

# Extracting the required data from dataset
convoFlow = []
for convo in conversation:
    convoFlow.append(convo.split(' +++$+++ ')[-1][1:-1].replace("'", " ").replace(",","").split())

dialog = {}
for line in lines:
    dialog[line.split(' +++$+++ ')[0]] = line.split(' +++$+++ ')[-1]

# Mapping Answers to Questions 
questions = []
answers = []

# Convo Replies(Answers) get mapped to Convos(Questions)
for convo in convoFlow:
    for i in range(len(convo) - 1):
        questions.append(dialog[convo[i]])
        answers.append(dialog[convo[i+1]])
        
# Deleting unused variables
del(convo, conversation , dialog, convoFlow, line, lines)   
        
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
    
for i in range(len(formattedAns)):
    formattedAns[i] = ' '.join(formattedAns[i].split()[:11])
    
# Deleting unused variables
del(answers, i , line, questions, sortedAns, sortedQues)   

# Limiting dataset to 30000 values
formattedQues = formattedQues[:30000]
formattedAns = formattedAns[:30000]

#Removing similar sentences
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
       
del(word, line)