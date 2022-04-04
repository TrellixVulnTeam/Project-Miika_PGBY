#Reading text files into variables
lines = open('dataset/lines.txt', encoding='utf-8', errors = 'ignore').read().split('\n')
conversation = open('dataset/conversations.txt', encoding='utf-8', errors = 'ignore').read().split('\n')

#Extracting the required data from dataset
convoFlow = []
for convo in conversation:
    convoFlow.append(convo.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(",","").split())
    
dialog = {}
for line in lines:
    dialog[line.split('+++$+++')[0]] = line.split('+++$+++')[-1]
    
#Mapping Answers to Questions    
questions = []
answers = []

#Convo Replies(Answers) get mapped to Convos(Questions)
for convo in convoFlow:
    for i in range(len(convo) - 1):
        questions.append(dialog[convo[i]])
        answers.append(dialog[convo[i+1]])
