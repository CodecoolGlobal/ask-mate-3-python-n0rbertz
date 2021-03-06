from psycopg2.extras import RealDictCursor
import database_common
import util


# GLOBAL
@database_common.connection_handler
def get_author_id(cursor: RealDictCursor, record_type, record_id) -> int:
    query = """
        SELECT user_id
        FROM [RT]
        WHERE id = %s""".replace('[RT]', record_type)
    cursor.execute(query, [record_id])
    ids = cursor.fetchall()
    author_id = ids[0]['user_id']

    return int(author_id) if author_id is not None else False


# VOTES
@database_common.connection_handler
def get_vote(cursor: RealDictCursor, record_type, question_id):
    query = """
        SELECT *
        FROM vote
        WHERE [RT]_id = %s""".replace('[RT]', record_type)

    cursor.execute(query, [int(question_id)])

    votes = cursor.fetchall()
    vote_count = 0
    for vote in votes:
        vote_count += int(vote['value'])

    return vote_count


@database_common.connection_handler
def get_user_vote(cursor: RealDictCursor, record_type, question_id):
    user_data = util.user_logged_in()
    if user_data is False:
        return 0

    query = """
        SELECT *
        FROM vote
        WHERE user_id = %s AND [RT]_id = %s
        LIMIT 1""".replace('[RT]', record_type)

    cursor.execute(query, [int(user_data['id']), int(question_id)])
    vote = cursor.fetchall()

    return int(vote[0]['value']) if len(vote) > 0 else 0


@database_common.connection_handler
def vote_record(cursor: RealDictCursor, record_type, record_id, vote_value=1):
    user_data = util.user_logged_in()
    if user_data is False:
        return

    query = """
        SELECT *
        FROM vote
        WHERE [RT]_id = %s AND user_id = %s""".replace('[RT]', record_type)
    cursor.execute(query, [record_id, user_data['id']])
    user_votes = cursor.fetchall()

    if len(user_votes) == 0:

        # NEW VOTE RECORD
        author_id = get_author_id(record_type, record_id)

        if author_id is False:
            return

        query = """INSERT INTO vote
            (vote_id, user_id, [RT]_id, value, author_id)
            VALUES(DEFAULT, %s, %s, %s, %s)""".replace('[RT]', record_type)

        cursor.execute(query, [user_data['id'], record_id, vote_value, author_id])

    elif len(user_votes) == 1:
        vote_id = user_votes[0]['vote_id']
        old_vote_value = user_votes[0]['value']

        if int(old_vote_value) != int(vote_value):

            # UPDATE VOTE RECORD
            query = """
                UPDATE vote
                SET value = %s
                WHERE vote_id = %s"""
            cursor.execute(query, [vote_value, vote_id])
        else:

            # DELETE VOTE RECORD
            query = """
                DELETE FROM vote
                WHERE vote_id = %s"""
            cursor.execute(query, [vote_id])


# QUESTIONS
def additional_question_data(question_data):
    question = question_data.copy()

    question['vote_number'] = get_vote('question', question['id'])
    question['user_vote'] = get_user_vote('question', question['id'])

    return question


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC"""
    # todo: why tho?
    # LIMIT 5"""
    cursor.execute(query)

    questions = cursor.fetchall().copy()

    for question_index in range(len(questions)):
        questions[question_index] = additional_question_data(questions[question_index])

    return questions


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id) -> list:
    query = """ 
        SELECT *
        FROM question
        WHERE id = %s"""
    # todo: order by vote table join
    # ORDER BY vote_number DESC"""
    cursor.execute(query, [question_id])
    # return cursor.fetchall()

    questions = cursor.fetchall().copy()

    for question_index in range(len(questions)):
        questions[question_index] = additional_question_data(questions[question_index])

    return questions


@database_common.connection_handler
def get_questions_by_search_phrase(cursor: RealDictCursor, search_phrase):
    query = """
    SELECT *
    FROM question
    WHERE title LIKE %s or message LIKE %s"""
    cursor.execute(query, ['%' + search_phrase + '%', '%' + search_phrase + '%'])
    # return cursor.fetchall()

    questions = cursor.fetchall().copy()

    for question_index in range(len(questions)):
        questions[question_index] = additional_question_data(questions[question_index])

    return questions


@database_common.connection_handler
def get_corresponding_question_id_of_answer_by_search_phrase(cursor: RealDictCursor, search_phrase):
    query = """
        SELECT question_id
        FROM answer
        WHERE message LIKE %s"""
    cursor.execute(query, ['%' + search_phrase + '%'])
    return cursor.fetchall()


@database_common.connection_handler
def get_question_of_question_id_for_search(cursor: RealDictCursor, question_id):
    placeholders = ', '.join(['%s'] * len(question_id))
    query = """SELECT *
    FROM question
    WHERE id IN ({})""".format(placeholders)
    cursor.execute(query, tuple(question_id))
    # return cursor.fetchall()

    questions = cursor.fetchall().copy()

    for question_index in range(len(questions)):
        questions[question_index] = additional_question_data(questions[question_index])

    return questions


@database_common.connection_handler
def add_question(cursor: RealDictCursor, submission_time, title, message, image):
    user_data = util.user_logged_in()
    if user_data is False:
        return

    query = """INSERT INTO question
    VALUES(DEFAULT, %s, 1, %s, %s, %s, %s)
    RETURNING id"""
    cursor.execute(query, [submission_time, title, message, image, int(user_data['id'])])
    return int(cursor.fetchone()['id'])


def vote_up_question(question_id):
    vote_record("question", question_id, 1)


def vote_down_question(question_id):
    vote_record("question", question_id, -1)


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, new_title, new_message, question_id,):
    query = """UPDATE question
    SET title = %s, message = %s
    WHERE id = %s"""
    cursor.execute(query, [new_title, new_message, int(question_id)])


@database_common.connection_handler
def delete_question_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %s"""
    cursor.execute(query, [question_id])


# ANSWERS
def additional_answer_data(answer_data):
    answer = answer_data.copy()

    answer['vote_number'] = get_vote('answer', answer['id'])
    answer['user_vote'] = get_user_vote('answer', answer['id'])

    return answer


@database_common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """ 
        SELECT answer.*, "user".email
        FROM answer
        JOIN "user" ON answer.user_id = "user".id
        WHERE question_id = %s"""
    # todo: ordering with joins
    # ORDER BY vote_number DESC"""
    cursor.execute(query, [question_id])
    # return cursor.fetchall()

    answers = cursor.fetchall().copy()

    for answer_index in range(len(answers)):
        answers[answer_index] = additional_answer_data(answers[answer_index])

    return answers


@database_common.connection_handler
def get_answer_id_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT id
        FROM answer
        WHERE question_id = %s"""
    cursor.execute(query, [int(question_id)])
    dictrow_answer_ids = cursor.fetchall()
    answer_ids = []
    for answer in dictrow_answer_ids:
        answer_ids.append(answer['id'])
    return answer_ids


@database_common.connection_handler
def get_question_id_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """
            SELECT question_id
            FROM answer
            WHERE id = %s
            LIMIT 1"""
    cursor.execute(query, [int(answer_id)])
    question_ids = cursor.fetchall()
    if len(question_ids) != 1:
        return False

    return int(question_ids[0]['question_id'])


@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, [answer_id])
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, submission_time, question_id, message, image):
    user_data = util.user_logged_in()

    if user_data is False:
        return

    query = """INSERT INTO answer
    VALUES(DEFAULT, %s, %s, %s, %s, %s)
    RETURNING id"""
    cursor.execute(query, [submission_time, int(question_id), message, image, user_data['id']])
    return int(cursor.fetchone()['id'])


def vote_up_answer(answer_id):
    vote_record("answer", answer_id, 1)


def vote_down_answer(answer_id):
    vote_record("answer", answer_id, -1)


@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, message, answer_id):
    query = """
    UPDATE answer
    SET message = %s
    WHERE id = %s"""
    cursor.execute(query, [message, answer_id])


@database_common.connection_handler
def delete_answer_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """
    DELETE FROM answer
    WHERE id = %s"""
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def delete_answer_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])


# COMMENTS
@database_common.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor, question_id):
    query = """SELECT comment.*, "user".email
    FROM comment
    JOIN  "user" ON comment.user_id = "user".id
    WHERE question_id = %s"""
    cursor.execute(query, [int(question_id)])
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_comment_id(cursor: RealDictCursor, comment_id):
    query = """
        SELECT question_id, answer_id
        FROM comment
        WHERE id = %s"""
    cursor.execute(query, [comment_id])
    comment_ids = cursor.fetchall()

    if len(comment_ids) != 1:
        return False

    if comment_ids[0]['question_id'] is not None:
        return int(comment_ids[0]['question_id'])

    return get_question_id_by_answer_id(int(comment_ids[0]['answer_id']))


@database_common.connection_handler
def get_comments_by_answer_ids(cursor: RealDictCursor, answer_ids):
    placeholders = ', '.join(['%s'] * len(answer_ids))
    query = """
        SELECT comment.*, "user".email
        FROM comment
        JOIN  "user" ON comment.user_id = "user".id
        WHERE answer_id IN ({})
        ORDER BY submission_time""".format(placeholders)
    cursor.execute(query, tuple(answer_ids))
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %s"""
    cursor.execute(query, [comment_id])
    return cursor.fetchall()


@database_common.connection_handler
def add_comment_to_question(cursor: RealDictCursor, question_id, message, submission_time):
    user_data = util.user_logged_in()
    if user_data is False:
        return

    query = """INSERT INTO comment
    (id, question_id, message, submission_time, user_id)
    VALUES(DEFAULT, %s, %s, %s, %s)"""
    cursor.execute(query, [int(question_id), message, submission_time, user_data['id']])


@database_common.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, answer_id, message, submission_time):
    user_data = util.user_logged_in()
    if user_data is False:
        return

    query = """
    INSERT INTO comment
    (id, answer_id, message, submission_time, user_id)
    VALUES(DEFAULT, %s, %s, %s, %s)"""
    cursor.execute(query, [int(answer_id), message, submission_time, user_data['id']])


@database_common.connection_handler
def edit_comment(cursor: RealDictCursor, message, comment_id, new_submission_time):
    query = """
    UPDATE comment
    SET message = %s, submission_time = %s
    WHERE id = %s"""
    cursor.execute(query, [message, new_submission_time, comment_id])


@database_common.connection_handler
def delete_comments_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_comments_by_answer_id(cursor: RealDictCursor, answer_id):
    placeholders = ', '.join(['%s'] * len(answer_id))
    query = """
        DELETE FROM comment
        WHERE answer_id IN ({})""".format(placeholders)
    cursor.execute(query, tuple(answer_id))


@database_common.connection_handler
def delete_comment_by_id(cursor: RealDictCursor, comment_id):
    query = """
    DELETE FROM comment
    WHERE id = %s"""
    cursor.execute(query, [comment_id])


# TAGS
@database_common.connection_handler
def delete_question_tag_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])


# USERS
@database_common.connection_handler
def add_user(cursor: RealDictCursor, email, hashed_password, submission_time):
    query = """
    INSERT INTO "user"
    VALUES (DEFAULT, %s, %s, %s)"""
    cursor.execute(query, [email, hashed_password, submission_time])


@database_common.connection_handler
def get_user_login_data(cursor: RealDictCursor, email):
    query = """
    SELECT * FROM "user" 
    WHERE email = %s"""
    cursor.execute(query, [email])
    return cursor.fetchall()


@database_common.connection_handler
def get_user_reputation(cursor: RealDictCursor, user_id):
    query = """
        SELECT *
        FROM vote
        WHERE author_id = %s"""
    cursor.execute(query, [user_id])
    all_vote = cursor.fetchall()

    reputation = 0

    for vote in all_vote:
        vote_dir = int(vote['value'])

        if vote['question_id'] is not None:
            reputation += 5 if vote_dir == 1 else -2
        elif vote['answer_id'] is not None:
            reputation += 10 if vote_dir == 1 else -2

    return reputation


@database_common.connection_handler
def get_hashed_password_by_email(cursor: RealDictCursor, email):
    query = """
    SELECT hashed_password FROM "user"
    WHERE email = %s"""
    cursor.execute(query, [email])
    return cursor.fetchall()


@database_common.connection_handler
def get_users_data(cursor: RealDictCursor):
    query = """
        SELECT "user".id, "user".email, "user".submission_time,
        (SELECT COUNT(*) FROM question WHERE question.user_id = "user".id) as question_count,
        (SELECT COUNT(*) FROM answer WHERE answer.user_id = "user".id) as answer_count,
        (SELECT COUNT(*) FROM comment WHERE comment.user_id = "user".id) as comment_count
        FROM "user"
        INNER JOIN question ON "user".id = question.user_id
        INNER JOIN answer ON "user".id = answer.user_id
        INNER JOIN comment ON "user".id = comment.user_id
        GROUP BY "user".id, "user".email, "user".submission_time;"""
    cursor.execute(query)
    user_data = cursor.fetchall().copy()
    for user_index in range(len(user_data)):
        user_data[user_index] = additional_user_data(user_data[user_index])
    return user_data


@database_common.connection_handler
def get_user_data(cursor: RealDictCursor, user_id):
    query = """
        SELECT "user".id, "user".email, "user".submission_time,
        (SELECT COUNT(*) FROM question WHERE question.user_id = %s) as question_count,
        (SELECT COUNT(*) FROM answer WHERE answer.user_id = %s) as answer_count,
        (SELECT COUNT(*) FROM comment WHERE comment.user_id = %s) as comment_count
        FROM "user"
        INNER JOIN question ON "user".id = question.user_id
        INNER JOIN answer ON "user".id = answer.user_id
        INNER JOIN comment ON "user".id = comment.user_id
        WHERE "user".id = %s
        GROUP BY "user".id, "user".email, "user".submission_time;"""
    cursor.execute(query, [user_id, user_id, user_id, user_id])
    user_data = cursor.fetchall()
    if len(user_data) != 1:
        return False

    user = additional_user_data(user_data[0].copy())
    return user


def additional_user_data(user_data):
    user = user_data.copy()
    user["reputation"] = get_user_reputation(user["id"])
    return user
