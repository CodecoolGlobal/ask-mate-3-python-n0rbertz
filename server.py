
from flask import Flask, render_template, redirect, request, url_for
import data_manager
from datetime import datetime
from flask import Flask


app = Flask(__name__)



app.config['SECRET_KEY'] = 'dd9d469c72ee3c7c46772dc782eba502'


@app.route("/")
@app.route("/list")
def list_questions():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)



@app.route('/question/<question_id>')
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_comments_by_question_id(question_id)
    print(question_comments)
    return render_template('display_question.html', question=question, answers=answers, question_comments=question_comments)



@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_comments_by_answer_id(answer_id)
    data_manager.delete_answer_by_answer_id(answer_id)
    return redirect('/')



@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_tag_by_question_id(question_id)
    data_manager.delete_comments_by_question_id(question_id)
    answer_ids = data_manager.get_answer_id_by_question_id(question_id)
    if len(answer_ids) > 0:
        data_manager.delete_comments_by_answer_id(answer_ids)
    data_manager.delete_answer_by_question_id(question_id)
    data_manager.delete_question_by_question_id(question_id)
    return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_title = request.form["title"]
        new_message = request.form["message"]
        image = "None"
        data_manager.add_question(submission_time, new_title, new_message, image)
        return redirect('/')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = request.form['message']
        image = "None"
        data_manager.add_answer(submission_time, question_id, message, image)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html')


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect('/')



@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_message = request.form['message']
        data_manager.edit_question(new_title, new_message, question_id)
        return redirect('/')
    return render_template('edit_question.html')


@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id):
    data_manager.vote_up_answer(answer_id)
    return redirect ('/')

@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    data_manager.vote_down_answer(answer_id)
    return redirect('/')


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        message = request.form['message']
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_comment_to_question(question_id, message, submission_time)
        return redirect('/')
    return render_template('add_comment_to_question.html')


if __name__ == "__main__":
    app.run(debug=True)
