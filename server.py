
from flask import Flask, render_template, redirect, request, url_for
import data_manager
import data_handler
import re
from operator import itemgetter
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
    return render_template('display_question.html', question=question, answers=answers)



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
    data_manager.delete_comments_by_answer_id(answer_ids)
    data_manager.delete_answer_by_question_id(question_id)
    data_manager.delete_question_by_question_id(question_id)
    return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        questions = data_handler.get_data_from_file('sample_data/question.csv')
        questions = [x for x in questions if x != []]
        question_id = int(questions[-1][0]) + 1
        submission_time = 0
        new_title = request.form["title"]
        new_message = request.form["message"]
        new_question = [question_id, submission_time, 0, 0, new_title, new_message]
        data_handler.add_question('sample_data/question.csv', new_question)
        return redirect('/')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        answers = data_handler.get_data_from_file('sample_data/answer.csv')
        answers = [x for x in answers if x != []]
        id = int(answers[-1][0]) + 1
        submission_time = 0
        vote_number = 0
        message = request.form['message']
        image = ""
        new_answer = [id, submission_time, vote_number, question_id, message, image]
        answers.append(new_answer)
        data_handler.write_answers('sample_data/answer.csv', answers)
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
        questions = data_handler.get_data_from_file('sample_data/question.csv')
        questions = [x for x in questions if x != []]
        questions[int(question_id)][4] = request.form['title']
        questions[int(question_id)][5] = request.form['message']
        data_handler.write_questions('sample_data/question.csv', questions)
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




if __name__ == "__main__":
    app.run(debug=True)
