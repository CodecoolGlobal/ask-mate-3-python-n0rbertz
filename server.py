<<<<<<< HEAD
from flask import Flask, render_template, redirect, request, url_for
import data_handler

=======
from flask import Flask
>>>>>>> da9e982313df4226e8834071a4b6397627d5b861

app = Flask(__name__)


<<<<<<< HEAD
app.config['SECRET_KEY'] = 'dd9d469c72ee3c7c46772dc782eba502'


@app.route("/")
@app.route("/list")
def list_questions():
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    return render_template('list.html', questions=questions)


#@app.route('/question')
#def get_question_id():
    #return request.args['id']

@app.route('/question/<question_id>')
def display_question(question_id):
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    questions = [x for x in questions if x != []]
    answers = data_handler.get_data_from_file('sample_data/answer.csv')
    answers = [answer for answer in answers if answer != []]
    answers = [answer for answer in answers if answer[3] == question_id or answer[0] == "id"]
    for question in questions:
        if question[0] == question_id:
            title = question[4]
            message= question[5]
    return render_template('display_question.html', title=title, message=message, question_id=question_id, answers=answers)



@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    all_answers = data_handler.get_data_from_file('sample_data/answer.csv')
    all_answers = [x for x in all_answers if x != []]
    question_id = all_answers[int(answer_id)][3]
    all_answers.pop(int(answer_id))
    data_handler.write_answers('sample_data/answer.csv', all_answers)
    return redirect(url_for('display_question', question_id=question_id))



@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    questions = [x for x in questions if x != []]
    for index, question in enumerate(questions):
        if question[0] == question_id:
            questions.pop(index)
    for new_id, question in enumerate(questions[1:], 1):
        question[0] = new_id
    data_handler.write_questions('sample_data/question.csv', questions)
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
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    questions = [x for x in questions if x != []]
    questions[int(question_id)][3] = int(questions[int(question_id)][3]) + 1
    data_handler.write_questions('sample_data/question.csv', questions)
    return redirect('/')



@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    questions = [x for x in questions if x != []]
    questions[int(question_id)][3] = int(questions[int(question_id)][3]) -1
    data_handler.write_questions('sample_data/question.csv', questions)
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
    answers = data_handler.get_data_from_file('sample_data/answer.csv')
    answers = [x for x in answers if x != []]
    answers[int(answer_id)][2] = int(answers[int(answer_id)][2]) + 1
    data_handler.write_answers('sample_data/answer.csv', answers)
    return redirect(url_for('display_question', question_id=answers[int(answer_id)][3]))

@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    answers = data_handler.get_data_from_file('sample_data/answer.csv')
    answers = [x for x in answers if x != []]
    answers[int(answer_id)][2] = int(answers[int(answer_id)][2]) - 1
    data_handler.write_answers('sample_data/answer.csv', answers)
    return redirect(url_for('display_question', question_id=answers[int(answer_id)][3]))




if __name__ == "__main__":
    app.run(debug=True)
=======
@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
>>>>>>> da9e982313df4226e8834071a4b6397627d5b861
