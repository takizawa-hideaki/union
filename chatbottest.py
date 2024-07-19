from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request
Chatbot = ChatBot('Bot thong minh',
                  storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                  database_uri='mongodb+srv://tongduylinh1995a:<password>@cluster0.iqvxauq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0wroh0ov-shard-00-02.iqvxauq.mongodb.net:27017/?ssl=true&replicaSet=atlas-marom9-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
trainer = ChatterBotCorpusTrainer(Chatbot)
trainer.train("chatterbot.corpus.english")
response = Chatbot.get_response("Hello World!")
print(response)
from chatterbot.trainers import ListTrainer
trainer = ListTrainer(Chatbot)
trainer.train([
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You're welcome."
])
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(Chatbot.get_response(userText))

if __name__ == "__main__":
    app.run()
