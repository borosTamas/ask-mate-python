from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
def render_index():
    questions = data_manager.collect_latest_5_question()
    return render_template('index.html', questions=questions)


@app.route('/all_question')
def show_all_question():
    questions = data_manager.collect_questions()
    return render_template('all_question.html', questions=questions)


@app.route('/question_page/vote',methods=['GET','POST'])
def vote():
    vote = int(request.form.get('vote_num'))
    vote_up = request.form.get('vote_up')
    vote_down = request.form.get('vote_down')
    q_id = request.form.get('q_id')
    if request.method == 'POST':
        if vote_up == 'up':
            vote += 1
        elif vote_down == 'down':
            vote -= 1
        data_manager.update_vote_number(vote=vote, q_id=q_id)
        return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    question_data = request.form.get('question_data')
    print(question_data)
    result = data_manager.find_searched_questions(searched_data=question_data)
    print(result)
    return render_template('all_question.html', questions=result)


@app.route('/question_page/<question_id>')
def show_question(question_id):
    question = data_manager.find_question(q_id=question_id)
    answers = data_manager.collect_answers(q_id=question_id)
    data_manager.update_view_number(q_id=question_id)
    return render_template('question_page.html', question=question, answers=answers)


@app.route('/question_page/<question_id>/edit')
def edit_question(question_id):
    result = data_manager.find_question(q_id=question_id)
    return render_template('add_question.html', result=result)


@app.route('/rewrite_question', methods=['POST'])
def rewrite_question():
    updated_question = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'view_number': request.form.get('view_number'),
        'vote_number': request.form.get('vote_number'),
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'image': request.form.get('image')
    }
    data_manager.update_question(datas=updated_question)
    return redirect('/')


@app.route('/question_page/<question_id>/new-answer', methods=['GET','POST'])
def post_an_answer(question_id):
    result = []
    message = ""
    if request.method=='POST':
        new_answer = create_answer(question_id, request.form['message'], request.form['image'])
        data_manager.add_answer(form_data=new_answer)
        return redirect('/')
    question = data_manager.find_question(question_id)
    return render_template('new_answer.html', question=question, result=result, message=message)



def create_answer(question_id, message, image):
    return {
        'submission_time': data_manager.submission_time_generator(),
        'vote_number': 1,
        'question_id': question_id,
        'message': message,
        'image': image
    }


@app.route('/question_page/<answer_id>/update')
def edit_answer(answer_id):
    result = data_manager.find_answer(a_id=answer_id)
    return render_template('new_answer.html', result=result)


@app.route('/rewrite_answer', methods=['POST'])
def rewrite_answer():
    updated_answer = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'vote_number': request.form.get('vote_number'),
        'question_id': request.form.get('question_id'),
        'message': request.form.get('message'),
        'image': request.form.get('image'),
    }
    data_manager.update_answer(datas=updated_answer)
    return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    result = []
    message = ""
    if request.method == 'POST':
        new_question = create_question(request.form['message'], request.form['image'], request.form['title'])
        data_manager.add_question(from_data=new_question)
        return redirect('/')
    return render_template('add_question.html', result=result, message=message)


def create_question(message, image, title):
    return {
        'submission_time': data_manager.submission_time_generator(),
        'vote_number': 1,
        'message': message,
        'title': title,
        'image': image,
        'view_number' : 1
    }



if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
