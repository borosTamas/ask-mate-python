from flask import Flask, render_template
import data_manager
app = Flask(__name__)

@app.route('/')
def render_index():
    questions = data_manager.collect_questions()
    return render_template('index.html', questions=questions)

@app.route('/question_page/<id>')
def show_question(id):
    question = question_data
    return render_template('question_page/<id>', question=question)


if __name__=="__main__":
    app.run(
        debug=True,
        port=5000
    )
