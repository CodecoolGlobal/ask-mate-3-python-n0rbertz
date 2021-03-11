from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = %s"""
    cursor.execute(query, [question_id])
    return cursor.fetchall()

@database_common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query=""" 
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = %s"""
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




