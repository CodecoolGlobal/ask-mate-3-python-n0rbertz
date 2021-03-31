from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, submission_time, view_number, title, message, image
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = %s
        ORDER BY vote_number DESC"""
    cursor.execute(query, [question_id])
    return cursor.fetchall()

@database_common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = %s
        ORDER BY vote_number DESC"""
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %s"""
    cursor.execute(query, [question_id])

@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %s"""
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_question_tag_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])

@database_common.connection_handler
def delete_comments_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])

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
def delete_comments_by_answer_id(cursor: RealDictCursor, answer_id):
    placeholders = ', '.join(['%s'] * len(answer_id))
    query = """
        DELETE FROM comment
        WHERE answer_id IN ({})""".format(placeholders)
    cursor.execute(query, tuple(answer_id))


@database_common.connection_handler
def delete_answer_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %s"""
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_question_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %s"""
    cursor.execute(query, [question_id])


@database_common.connection_handler
def delete_answer_by_answer_id(cursor: RealDictCursor, answer_id):
    query="""
    DELETE FROM answer
    WHERE id = %s"""
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, answer_id):
    query=""" 
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %s"""
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, answer_id):
    query=""" 
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %s"""
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def add_question(cursor: RealDictCursor, submission_time, title, message, image):
    query="""INSERT INTO question
    VALUES(DEFAULT, %s, 1, 0, %s, %s, %s)"""
    cursor.execute(query, [submission_time, title, message, image])

@database_common.connection_handler
def add_answer(cursor: RealDictCursor, submission_time, question_id, message, image):
    query="""INSERT INTO answer
    VALUES(DEFAULT, %s, 0, %s, %s, %s)"""
    cursor.execute(query, [submission_time, int(question_id), message, image])


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, new_title, new_message, question_id,):
    query="""UPDATE question
    SET title = %s, message = %s
    WHERE id = %s"""
    cursor.execute(query, [new_title, new_message, int(question_id)])


@database_common.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor, question_id):
    query="""SELECT id, submission_time, message
    FROM comment
    WHERE question_id = %s"""
    cursor.execute(query, [int(question_id)])
    return cursor.fetchall()

@database_common.connection_handler
def add_comment_to_question(cursor: RealDictCursor, question_id, message, submission_time):
    query="""INSERT INTO comment
    (id, question_id, message, submission_time)
    VALUES(DEFAULT, %s, %s, %s)"""
    cursor.execute(query, [int(question_id), message, submission_time])

@database_common.connection_handler
def get_comments_by_answer_ids(cursor: RealDictCursor, answer_ids):
    placeholders = ', '.join(['%s'] * len(answer_ids))
    query = """
        SELECT id, answer_id, submission_time, message, edited_count
        FROM comment
        WHERE answer_id IN ({})""".format(placeholders)
    cursor.execute(query, tuple(answer_ids))
    return cursor.fetchall()

@database_common.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, answer_id, message, submission_time):
    query="""
    INSERT INTO comment
    (id, answer_id, message, submission_time)
    VALUES(DEFAULT, %s, %s, %s)"""
    cursor.execute(query, [int(answer_id), message, submission_time])


@database_common.connection_handler
def get_questions_by_search_phrase(cursor: RealDictCursor, search_phrase):
    query="""
    SELECT id, submission_time, view_number, vote_number, title, message, image
    FROM question
    WHERE title LIKE %s or message LIKE %s"""
    cursor.execute(query, ['%' + search_phrase + '%', '%' + search_phrase + '%'])
    return cursor.fetchall()

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
    query="""SELECT id, submission_time, view_number, vote_number, title, message, image
    FROM question
    WHERE id IN ({})""".format(placeholders)
    cursor.execute(query, tuple(question_id))
    return cursor.fetchall()

@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, message, answer_id):
    query="""
    UPDATE answer
    SET message = %s
    WHERE id = %s"""
    cursor.execute(query, [message, answer_id])

@database_common.connection_handler
def edit_comment(cursor: RealDictCursor, message, comment_id, new_submission_time):
    query="""
    UPDATE comment
    SET message = %s, submission_time = %s
    WHERE id = %s"""
    cursor.execute(query, [message, new_submission_time, comment_id])

@database_common.connection_handler
def delete_comment_by_id(cursor: RealDictCursor, comment_id):
    query="""
    DELETE FROM comment
    WHERE id = %s"""
    cursor.execute(query, [comment_id])

@database_common.connection_handler
def add_user(cursor: RealDictCursor, email, hashed_password, submission_time):
    query = """
    INSERT INTO "user"
    VALUES (DEFAULT, %s, %s, %s)"""
    cursor.execute(query, [email, hashed_password, submission_time])

@database_common.connection_handler
def get_user_data(cursor: RealDictCursor, email):
    query="""
    SELECT * FROM "user" 
    WHERE email = %s"""
    cursor.execute(query, [email])
    return cursor.fetchall()

@database_common.connection_handler
def get_hashed_password_by_email(cursor: RealDictCursor, email):
    query="""
    SELECT hashed_password FROM "user"
    WHERE email = %s"""
    cursor.execute(query, [email])
    return cursor.fetchall()
