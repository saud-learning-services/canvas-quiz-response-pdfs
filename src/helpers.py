"""
QUIZ REPORTS: helpers

authors:
@markoprodanovic

last edit:
Monday, May 04, 2020
"""

from util import shut_down
from pathlib import Path
import pandas as pd
import settings
import requests
import settings
import random
import string
import time
import json
import io


def get_all_essay_question_ids(quiz_questions):

    # get the ones in the quiz (not in question banks!)
    essay_question_ids = _get_essay_question_ids(quiz_questions)

    if settings.has_question_bank:
        print("Getting question data from Question Bank...")
        # get all quiz submissions
        submissions = settings.quiz.get_submissions()
        for sub in submissions:
            submission_questions = sub.get_submission_questions()

            submission_essay_question_ids = _get_essay_question_ids(
                submission_questions
            )

            for question_id in submission_essay_question_ids:
                if question_id not in essay_question_ids:
                    essay_question_ids.append(question_id)

    return essay_question_ids


def _get_essay_question_ids(questions):
    essay_questions = list(
        filter(lambda q: (q.question_type == "essay_question"), questions)
    )
    only_ids = map(lambda q: (str(q.id)), essay_questions)

    ids = []
    for id in only_ids:
        ids.append(id)

    return ids


def create_quiz_report(base_url, course_id, quiz_id):
    url = f"{base_url}/api/v1/courses/{str(course_id)}/quizzes/{str(quiz_id)}/reports"

    payload = {
        "quiz_report[report_type]": "student_analysis",
        "quiz_report[includes_all_versions]": True,
    }

    r = requests.post(url, headers=settings.auth_header, data=payload)

    export_details = json.loads(r.text)

    return export_details


def get_progress(progress_url, attempt_number):
    # maximum 9 attempts (90 seconds) to get progress before shutting down with error
    if attempt_number >= 9:
        shut_down(
            "ERROR: Application timeout, Canvas quiz report is taking too long to generate. Try again in a few minutes."
        )

    r_progress = requests.get(progress_url, headers=settings.auth_header)
    progress_state = json.loads(r_progress.text)
    progress_completion = progress_state["workflow_state"]

    if progress_completion == "completed":
        return progress_completion
    elif progress_completion == "failed":
        raise Exception
    elif progress_completion == "queued" or progress_completion == "running":
        # set timeout for 10 seconds then try again
        print(f"Report state is: {progress_completion}, waiting...")
        time.sleep(10)
        return get_progress(progress_url, attempt_number + 1)
    else:
        shut_down(
            f"ERROR: Unrecognized value for workflow_state in Canvas: {progress_completion}."
        )


def download_quiz_report(report_info):
    # downloads the quiz reports and gathers info
    try:
        download_url = report_info["file"]["url"]
        filename = report_info["file"]["display_name"]
        res = requests.get(download_url, headers=settings.auth_header)
        report_path = Path(f"{settings.ROOT}/raw_reports/{filename}")

        with (open(report_path, "wb")) as output:
            output.write(res.content)
            print(f"Outputting Raw Report: {filename}\n")

        df = pd.read_csv(io.StringIO(res.content.decode("utf-8")))

        return df
    except Exception:
        shut_down("ERROR: Unable to download quiz report.")


def generate_random_id():
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(15)]
    )
