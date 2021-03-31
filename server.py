from flask import render_template, redirect, request, url_for, session
import data_manager
from datetime import datetime
from flask import Flask
import password_hasher
import util

app = Flask(__name__)


app.config['SECRET_KEY'] = 'dd9d469c72ee3c7c46772dc782eba502'


# HOME
@app.route("/")
@app.route("/list")
def list_questions():

    logged_in_user = util.user_logged_in()

    questions = data_manager.get_questions()
    return render_template('list.html', user=logged_in_user, questions=questions)


@app.route('/search', methods=['GET', 'POST'])
def search():

    logged_in_user = util.user_logged_in()

    if request.method == 'GET':
        search_phrase = request.args.get('search_phrase')
        print(search_phrase)
        questions=data_manager.get_questions_by_search_phrase(search_phrase)
        question_ids_of_answers = data_manager.get_corresponding_question_id_of_answer_by_search_phrase(search_phrase)
        question_ids = []
        for question in question_ids_of_answers:
            question_ids.append(question['question_id'])
        if len(question_ids) > 0:
            questions_of_answers = data_manager.get_question_of_question_id_for_search(question_ids)
            questions = questions + questions_of_answers
    return render_template('search_results.html', user=logged_in_user, questions=questions)


# USER MANAGEMENT
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        user_data = data_manager.get_user_data(email)

        if len(user_data) == 1:
            password = request.form["password"]
            hashed_password = data_manager.get_hashed_password_by_email(email)
            hashed_password = hashed_password[0]['hashed_password']
            if password_hasher.verify_password(password, hashed_password=hashed_password):
                session["user_data"] = util.pretty_user_data(user_data)

                # return redirect(url_for("list_question"))

                return "hello " + session["email"]
        else:
            return "Invalid username or password"
    return render_template('login.html', user=False)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = password_hasher.hash_password(password)
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_user(email=email, hashed_password=hashed_password, submission_time=submission_time)
        return redirect('/')
    return render_template('register.html', user=False)


# QUESTION MANAGEMENT
@app.route('/add-question', methods=['GET', 'POST'])
def add_question():

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_title = request.form["title"]
        new_message = request.form["message"]
        image = "None"
        data_manager.add_question(submission_time, new_title, new_message, image)
        return redirect('/')
    return render_template('add-question.html', user=logged_in_user)


@app.route('/question/<question_id>')
def display_question(question_id):

    logged_in_user = util.user_logged_in()

    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_comments_by_question_id(question_id)
    answer_ids = []
    answer_comments = []
    for answer in answers:
        answer_ids.append(answer['id'])
    if len(answer_ids) > 0:
        answer_comments = data_manager.get_comments_by_answer_ids(answer_ids)
    return render_template('display_question.html', user=logged_in_user, question=question, answers=answers, question_comments=question_comments, answer_comments=answer_comments)


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

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        new_title = request.form['title']
        new_message = request.form['message']
        data_manager.edit_question(new_title, new_message, question_id)
        return redirect('/')
    return render_template('edit_question.html', user=logged_in_user)


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


# ANSWER MANAGEMENT
@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = request.form['message']
        image = "None"
        data_manager.add_answer(submission_time, question_id, message, image)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', user=logged_in_user)


@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id):
    data_manager.vote_up_answer(answer_id)
    return redirect ('/')


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    data_manager.vote_down_answer(answer_id)
    return redirect('/')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        new_message = request.form['message']
        data_manager.edit_answer(new_message, answer_id)
        return redirect('/')
    return render_template('edit_answer.html', user=logged_in_user)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_comments_by_answer_id(answer_id)
    data_manager.delete_answer_by_answer_id(answer_id)
    return redirect('/')


# COMMENT MANAGEMENT
@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        message = request.form['message']
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_comment_to_question(question_id, message, submission_time)
        return redirect('/')
    return render_template('add_comment_to_question.html', user=logged_in_user)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        message = request.form['message']
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_comment_to_answer(answer_id, message, submission_time)
        return redirect('/')
    return render_template('add_comment_to_answer.html', user=logged_in_user)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):

    logged_in_user = util.user_logged_in()

    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = request.form['message']
        data_manager.edit_comment(new_message, comment_id, submission_time)
        return redirect('/')
    return render_template('edit_comment.html', user=logged_in_user)


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    data_manager.delete_comment_by_id(comment_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
