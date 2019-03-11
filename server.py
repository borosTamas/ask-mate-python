from flask import Flask, render_template, request, redirect
import question_data_manager
import data_manager

app = Flask(__name__)


@app.route('/')
def render_index():
    questions = question_data_manager.collect_latest_5_question()
    return render_template('index.html', questions=questions)


@app.route('/all_question')
def show_all_question():
    questions = question_data_manager.collect_questions()
    return render_template('all_question.html', questions=questions)


@app.route('/all_question/sort',methods=['GET', 'POST'])
def show_all_sorted_question():
    questions = sort_questions()
    return render_template('all_question.html', questions=questions)


def sort_questions():
    sort_options = request.form.get('sort_options')
    option = request.form.get('options')
    result = question_data_manager.sort_questions(option=option, how=sort_options)
    return result


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


@app.route('/question_page/<question_id>/delete')
def delete_question(question_id):
    question_data_manager.delete_question(q_id=question_id)
    return show_all_question()
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


@app.route('/question_page/<question_id>/<answer_id>/answer-delete')
def delete_answer(question_id, answer_id):
    data_manager.delete_answer(q_id=question_id, a_id=answer_id)
    return show_question(question_id)


@app.route('/search', methods=['POST'])
def search():
    question_data = request.form.get('question_data')
    result = question_data_manager.find_searched_questions(searched_data=question_data)
    return render_template('all_question.html', questions=result)


@app.route('/question_page/<question_id>')
def show_question(question_id):
    question = question_data_manager.find_question(q_id=question_id)
    answers = data_manager.collect_answers(q_id=question_id)
    data_manager.update_view_number(q_id=question_id)
    comment = data_manager.collect_comment_to_question(q_id=question_id)
    answer_comment = []
    for answer in answers:
        temporary = data_manager.collect_comment_to_answer(a_id=answer['id'])
        if len(temporary)>0:
            answer_comment.append(temporary[0])
    return render_template('question_page.html', question=question, answers=answers, comment=comment, answer_comment=answer_comment)


@app.route('/question_page/<question_id>/edit')
def edit_question(question_id):
    result = question_data_manager.find_question(q_id=question_id)
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
    question_data_manager.update_question(datas=updated_question)
    return show_question(updated_question['id'])


@app.route('/question_page/<question_id>/new-answer', methods=['GET','POST'])
def post_an_answer(question_id):
    result = []
    message = ""
    if request.method=='POST':
        new_answer = create_answer(question_id, request.form['message'], request.form['image'])
        data_manager.add_answer(form_data=new_answer)
        return redirect('/')
    question = question_data_manager.find_question(question_id)
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
    return show_question(updated_answer['question_id'])


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    result = []
    message = ""
    if request.method == 'POST':
        new_question = create_question(request.form['message'], request.form['image'], request.form['title'])
        question_data_manager.add_question(from_data=new_question)
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


@app.route('/question_page/<question_id>/comment', methods=['GET','POST'])
def add_comment_to_question(question_id):
    comment = 'question'
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_comment_to_question(q_id=question_id, comment_message=message)

        return show_question(question_id)
    return render_template('add_comment.html', question_id=question_id, comment=comment)


@app.route('/question_page/<question_id>/<answer_id>/comment', methods=['GET','POST'])
def add_comment_to_answer(answer_id, question_id):
    comment = 'answer'
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_comment_to_answer(a_id=answer_id, comment_message=message)
        return show_question(question_id)
    return render_template('add_comment.html', answer_id=answer_id, question_id=question_id, comment=comment)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
