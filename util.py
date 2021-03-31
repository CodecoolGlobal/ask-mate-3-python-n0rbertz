from flask import session


def pretty_user_data(dict_row):

    result = {}

    for dict_key in dict_row[0]:
        result[dict_key] = dict_row[0][dict_key]

    return result


def user_logged_in():
    return session["user_data"] if "user_data" in session else False