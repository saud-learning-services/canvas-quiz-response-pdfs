"""
QUIZ REPORTS: interface

authors:
@markoprodanovic

last edit:
Wednesday, April 01, 2020
"""

import getpass
import settings
from util import shut_down
from canvasapi import Canvas
from termcolor import cprint


def get_user_inputs():
    """Prompt user for required inputs. Queries Canvas API throughout to check for
    access and validity errors. Errors stop execution and print to screen.

    Returns:
        Dictionary containing inputs
    """

    # prompt user for url and token
    url = input('Canvas Instance URL: ')
    token = getpass.getpass('Please enter your token: ')
    auth_header = {'Authorization': f'Bearer {token}'}

    # Canvas object to provide access to Canvas API
    canvas = Canvas(url, token)

    # get user object
    try:
        user = canvas.get_user('self')
        cprint(f'\nHello, {user.name}!', 'green')
    except Exception:
        shut_down(
            """
            ERROR: could not get user from server.
            Please ensure token is correct and valid and ensure using the correct instance url.
            """
        )

    # get course object
    try:
        course_id = input('Course ID: ')
        course = canvas.get_course(course_id)
    except Exception:
        shut_down(
            f'ERROR: Course not found [ID: {course_id}]. Please check course number.')

    # get students from course
    try:
        students = course.get_users(enrollment_type='student')
    except Exception:
        shut_down(
            'ERROR: Not able to get students from course. Ensure course has enrolled students.')

    # get the quiz from course
    try:
        quiz_id = input('Quiz ID: ')
        quiz = course.get_quiz(quiz_id)
    except Exception:
        shut_down(
            f'ERROR: Quiz not found [ID: {quiz_id}]. Please check quiz number.')

    # prompt user for confirmation
    _prompt_for_confirmation(user.name, course.name, quiz.title)

    # set course, quiz, students and auth_header as global variables
    settings.course = course
    settings.quiz = quiz
    settings.students = students
    settings.auth_header = auth_header

    # return inputs dictionary
    return url, course_id, quiz_id


def _prompt_for_confirmation(user_name, course_name, quiz_title):
    """Prints user inputs to screen and asks user to confirm. Shuts down if user inputs
    anything other than 'Y' or 'y'. Returns otherwise.

    Args:
        user_name (string): name of user (aka. holder of token)
        course_name (string): name of course returned from Canvas
        quiz_name (string): name of quiz returned from Canvas course object

    Returns:
        None -- returns only if user confirms

    """
    cprint('\nConfirmation:', 'blue')
    print(f'USER:  {user_name}')
    print(f'COURSE:  {course_name}')
    print(f'QUIZ:  {quiz_title}')
    print('\n')

    confirm = input(
        'Would you like to continue using the above information?[y/n]: ')

    print('\n')

    if confirm is 'y' or confirm is 'Y':
        return
    elif confirm is 'n' or confirm is 'N':
        shut_down('Exiting...')
    else:
        shut_down('ERROR: Only accepted values are y and n')