from flask import Flask, render_template
import data_manager
app = Flask(__name__)

@app.route('/')
def render_index():
    questions = data_manager.collect_questions()
    return render_template('index.html', questions=questions)

@app.route('/add-question')
def add_question():
    pass

@app.route('/question/<question_id>/new-answer')
def post_an_answer():
    pass



if __name__=="__main__":
    app.run(
        debug=True,
        port=5000
    )
