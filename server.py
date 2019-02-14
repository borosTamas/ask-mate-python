from flask import Flask, render_template,request, redirect
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

@app.route('/question_page/<id>/edit')
def edit_question(id):
    result = data_manager.find_question(id)
    return render_template('add_question.html', result=result)

@app.route('/rewrite_question', methods=['POST'])
def rewrite_suestion():
    updated_question = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'view_number': request.form.get('view_number'),
        'vote_number': request.form.get('vote_number'),
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'image': request.form.get('image')
    }
    data_manager.update_question(updated_question)
    return redirect('/')


@app.route('/question_page/<id>/new-answer', methods=['GET','POST'])
def post_an_answer(id):
    saved_data = {}
    question = data_manager.find_question(id)
    answer = data_manager.collect_answers(id)
    if request.method == 'POST':
        saved_data['id'] = data_manager.id_generator()
        saved_data['submission_time'] = data_manager.submission_time_generator()
        saved_data['vote_number'] = 1
        saved_data['question_id'] = request.form['question']
        saved_data['message'] = request.form['message']
        saved_data['image'] = request.form['image']
        data_manager.add_answer(saved_data)
        return redirect('/')
    return render_template('new_answer.html', question=question, answer=answer)


@app.route('/add-question',methods=['GET','POST'])
def route_index():
    result = []
    if request.method == 'POST':

        question_name = request.form.get('question_name')
        question = request.form.get('question')
        data_manager.csv_questionwriter('sample_data/question.csv',question_name,question)
        return redirect('/')
    return render_template('add_question.html', result=result)


@app.route('/question_page/<id>/edit_question')
def edit_question(id):
    question = data_manager.find_question(id)
    return render_template('edit_question.html', question=question)


if __name__=="__main__":
    app.run(
        debug=True,
        port=5000
    )
