from flask import Flask, render_template,request
import data_manager
app = Flask(__name__)

@app.route('/')
def render_index():
    questions = data_manager.collect_questions()
    return render_template('index.html', questions=questions)


@app.route('/question_page/<id>')
def show_question(id):
    question = data_manager.find_question(id)
    answers = data_manager.collect_answers(id)
    return render_template('question_page.html', question=question, answers=answers)


@app.route('/add-question',methods=['GET','POST'])
def route_index():
    if request.method == 'POST':
        result = request.form.get('question')
        result2 = request.form.get('question_name')
        print(result)
        print(result2)
    return render_template('add_question.html')


if __name__=="__main__":
    app.run(
        debug=True,
        port=5000
    )
