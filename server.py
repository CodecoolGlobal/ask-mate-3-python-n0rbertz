
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
    answer_ids = []
    answer_comments = []
    for answer in answers:
        answer_ids.append(answer['id'])
    if len(answer_ids) > 0:
        answer_comments = data_manager.get_comments_by_answer_ids(answer_ids)
    return render_template('display_question.html', question=question, answers=answers, question_comments=question_comments, answer_comments=answer_comments)



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


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        message = request.form['message']
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_comment_to_answer(answer_id, message, submission_time)
        return redirect('/')
    return render_template('add_comment_to_answer.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_phrase = request.form['search_phrase']
        questions=data_manager.get_questions_by_search_phrase(search_phrase)
        question_ids_of_answers = data_manager.get_corresponding_question_id_of_answer_by_search_phrase(search_phrase)
        question_ids = []
        for question in question_ids_of_answers:
            question_ids.append(question['question_id'])
        if len(question_ids) > 0:
            questions_of_answers = data_manager.get_question_of_question_id_for_search(question_ids)
            questions = questions + questions_of_answers
    return render_template('search_results.html', questions=questions)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        new_message = request.form['message']
        data_manager.edit_answer(new_message, answer_id)
        return redirect('/')
    return render_template('edit_answer.html')


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = request.form['message']
        data_manager.edit_comment(new_message, comment_id, submission_time)
        return redirect('/')
    return render_template('edit_comment.html')


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    data_manager.delete_comment_by_id(comment_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
