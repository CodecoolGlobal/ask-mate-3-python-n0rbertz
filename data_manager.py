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
    cursor.execute(query, [int(question_id)+1])
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
