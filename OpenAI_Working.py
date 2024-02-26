from flask import Flask, request, jsonify, render_template, session, redirect, flash
import openai
import os

app = Flask(__name__)
app.secret_key = 'hellohowareyou'
API = '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'
openai.api_key = API
t = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            text = file.read().decode("utf-8")
            file.save("uploads/"+file.filename)
            global t
            t = text
            filename=file.filename
        return render_template("home.html", message="Success ! \n Awaiting new upload ...", filename=filename)
    return render_template("home.html", message="Awaiting Upload ...")


@app.route('/getSummary', methods=['POST'])
def getSummary():
    prompt = "from this text supplied here please without any further introduction give a summary of the text with heading SUMMARY :  \n"
    global t
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    return completion.choices[0].message["content"]


@app.route('/getQuestionAndAnswer', methods=['POST'])
def getQuestionAndAnswer():
    prompt = "Based on the text supplied here, please provide five questions and their answerswith without any introduction. For each question and answer set, use the format QUESTION=question ANSWER=answer , and include the marker 'NEW-QUESTION-BEGINS' to start a new question and answer set. 'QUESTION' and 'ANSWER'should be in uppercase letters and always be followed by = (equal to ) sign. NEW LINE AFTER EVERY QUESTION MARK.Provide heading Q&A at the top. Avoid any additional introduction beyond the instructions outlined here. Here is the supplied text:  "
    global t
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    return completion.choices[0].message["content"]


@app.route('/getGlossary', methods=['POST'])
def getGlossary():
    prompt = "Please upfront (without any introduction) based on the text supplied here, give a set of five glossary terms and their definitions. For the 1st glossary term, you would respond like TERM=First term DEFINITION: definition of first term. For the 2nd glossary term, you would respond like TERM= 2nd term DEFINITION: Definition of 2nd term and so on. After each term and definition set, please include the marker 'NEW-TERM-BEGINS' to start a new glossary term. Please remember that 'TERM' , 'DEFINITION' and 'NEW-TERM-BEGINS' should always be in uppercase letters. Henceforth your output will be like TERM=First term DEFINITION: definition of first term NEW-TERM-BEGINS TERM= 2nd term DEFINITION: Definition of 2nd term NEW-TERM-BEGINS TERM= 3rd term DEFINITION: Definition of 3rd term and so on . Provide heading GLOSSARY in the starting. "
    global t
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    return completion.choices[0].message["content"]


@app.route('/getQuestionMultipleChoice', methods=['POST'])
def getQuestionMultipleChoice():
    prompt = "Please generate 5 multiple choice questions based on the text provided here. The questions should have 4 options each, and the options should be denoted by A), B), C), and D). Please ensure that each question ends with a question mark (?).Give the answer in the last line after options for every question. For example: Q1) What is the capital of France? A) London B) Paris C) Rome D) Berlin. Begin each question with 'Q' followed by a number, and separate the options with a comma. After each question, please include the marker 'NEW-QUESTION-BEGINS' to start a new question. There should be no additional introduction beyond the instructions outlined here. The supplied text is: "
    global t
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    return completion.choices[0].message["content"]


if __name__ == '__main__':
    app.run()
