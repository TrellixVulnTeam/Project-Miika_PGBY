from flask import Flask, jsonify, request
import random
import json
import torch
from app.nltk_utils import word_bank, tokenize
from app.model import NeuralNet

app = Flask(__name__)

try:
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

	with open('app/intents.json', 'r') as f:
		intents = json.load(f)

	FILE = "app/miika_model.pth"
	data = torch.load(FILE)

	input_size = data["input_size"]
	hidden_size = data["hidden_size"]
	output_size = data["output_size"]
	all_words = data["all_words"]
	tags = data["tags"]
	model_state = data["model_state"]

	model = NeuralNet(input_size, hidden_size, output_size).to(device)
	model.load_state_dict(model_state)
	model.eval()

except Exception as e:
	print(e)

@app.route('/')
def index():
	return "<h1>Deployed to Heroku</h1>"



@app.route('/chatbot', methods=["GET","POST"])
def chatbot_msg():
	
		user_data = request.json

		sentence = user_data['message']
	
		sentence = tokenize(sentence)
		X = word_bank(sentence, all_words)
		X = X.reshape(1, X.shape[0])
		X = torch.from_numpy(X)

		output = model(X)
		_, predicted = torch.max(output, dim=1)
		tag = tags[predicted.item()]
		probs = torch.softmax(output, dim=1)
		prob = probs[0][predicted.item()]

		if prob.item() > 0.75:
			for intent in intents["intents"]:
				if tag == intent["tag"]:
					msg=random.choice(intent['responses'])
			
					return jsonify(msg)
		else:
			return jsonify("I do not understand...")

@app.route("/test",methods=["GET","POST"])
def test():
	x = {"a":1,
		"b":2,
		"c":3}
	return jsonify(x)

if __name__ == '__main__':
	app.run(port=5000, debug=True)
