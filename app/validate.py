import re
from flask import jsonify
import datetime

now = datetime.datetime.now()


def validate_actor(data):
    # validate name
    if validate_name(data):
        return validate_name(data)

    # validate age
    if validate_age(data):
        return validate_age(data)

    # validate gender
    if validate_gender(data):
        return validate_gender(data)


def validate_movie(data):
    # validate title
    if validate_title(data):
        return validate_title(data)

    # validate date
    if validate_date(data):
        return validate_date(data)


def validate_name(data):
    """Validate name:
            should be more than 3 alphabets
            allow space in between name
            allow any case of letters
    """
    if not re.match(r'^[a-zA-Z ]{3,}$', data['name']):
        msg = "Name should have alphabets only with more than 3 characters"
        return jsonify({'message': msg}), 400


def validate_age(data):
    """Validate age"""
    if (data['age'] < 1 or data['age'] > 105):
        msg = "Please input a valid age between 1-105!"
        return jsonify({'message': msg}), 400


def validate_gender(data):
    """Validate gender:
            should be male, female or other
    """
    g = data['gender'].rstrip().title()
    if (g != "Male" and g != "Female" and g != "Other"):
        msg = "Gender should be Male, Female or Other"
        return jsonify({'message': msg}), 400


def validate_date(data):
    """Validate date"""
    try:
        if datetime.datetime.strptime(data['release_date'], '%d-%m-%Y'):
            pass
    except:
        msg = "Date should be in the format %DD-%MM-%YYYY"
        return jsonify({'message': msg}), 400

    if datetime.datetime.strptime(data['release_date'], '%d-%m-%Y') < now:
        msg = "Date cannot be earlier than today or now"
        return jsonify({'message': msg}), 400


def validate_title(data):
    """Validate title:
            should not be less than one character
            allow space in between name
            allow any case of letters
    """
    if not re.match(r'^[a-zA-Z0-9 ]{1,}$', data['title']):
        msg = "title should contain atleat a letters or a numbers only"
        return jsonify({'message': msg}), 400
