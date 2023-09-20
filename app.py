import csv 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

MAX_QUESTIONS = 5

questions = []
with open('engg_test_questions.csv') as file:
  reader = csv.DictReader(file)
  for row in reader:
     row['answered'] = False
     questions.append(row)

questions.sort(key=lambda x: float(x['difficulty']))

@app.route("/")  
def index():
  return render_template("index.html")

@app.route("/start", methods=['POST'])  
def start():
  global question_ids

  
  first_q = questions[len(questions)//2]
  question_ids = [first_q]

  return redirect(url_for('question'))

@app.route("/question")
def question():
  if len(question_ids) >= MAX_QUESTIONS+1:
     return redirect(url_for('result'))

  q = get_next_question()
  if q is None:
     return redirect(url_for('result'))

  question_ids.append(q)
  return render_template("question.html", q=q)

def get_next_question():
  if len(question_ids) == 0:
    return questions[len(questions)//2]
  
  last_q = question_ids[-1]
  last_index = questions.index(last_q)

  if last_q['answered']:
    del questions[last_index]
    next_index = last_index + 1
  else:
    del questions[last_index]
    next_index = last_index - 1
  
  if next_index < len(questions):
     return questions[next_index]
  else:
     return None

@app.route("/check", methods=["POST"])
def check():
  q = question_ids[-1]
  q['answered'] = request.form['answer'] == q['answer']

  return redirect(url_for('question'))

@app.route("/result")
def result():
  score = len([q for q in question_ids if q['answered']]) 
  ability = get_ability(score)

  return render_template("result.html", score=score, ability=ability)

def get_ability(score):
  if score >= 4:
    return "High"
  elif score >= 3:
    return "Medium"
  else: 
    return "Low"

if __name__ == "__main__":
  app.run(debug=True)