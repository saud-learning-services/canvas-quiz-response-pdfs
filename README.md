# Quiz Reports

> Quiz Reports is in BETA. Use at own risk. We are constantly improving performance, usability, and stability.

## Summary

**Quiz Reports** is a Jupyter Notebook and Python application that pulls quiz data from [Canvas LMS](https://github.com/instructure/canvas-lms) to create PDF documents containing student answers to *essay questions*. Application requires the following user inputs:

* Canvas Instance
* Active Canvas Access Token
* Course ID
* Quiz ID
* Question Banks (users will need to specify whether or not the quiz uses Question Banks)

## Output

### `.zip` file containing a PDF per student *(who submitted the quiz)*

* **ID** (randomly-generated, anonymous student identifier)
* **Course name** (as it appears on Canvas)
* **Question text** (as it appears on Canvas)
* **Student's response** (all submitted text -- does not preserving formatting)

> NOTE: all of the above will repeat for as many questions as are in the quiz (on seperate pages)

### `.csv` detailing

* **Student Name** (as it appears on Canvas)
* **Student ID** (UBC student ID)
* **Canvas ID** (Canvas LMS ID)
* **Anonymous ID** (as it appears in the output PDFs)

> NOTE: this table contains sensitive information and should **NOT** be distributed or uploaded anywhere

## Important Caveats

* Only works for “Classic Quizzes” on Canvas (not New Quizzes)
* Formatting in the student response is **not** preserved
* Will only output questions of type “Essay Question” on Canvas
* Tool is designed for a *Final Exam* use case and therefore, **should not be run on Quizzes that allow more than one attempt.** Doing so may cause unexpected and/or unreliable behaviour.

## Getting Started

*Are you Sauder Operations Staff? Please see [Sauder Setup](sauder-ops-guide.md) for detailed instructions*

> Project uses **conda** to manage environment (See official **conda** documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file))

1. Clone **quiz_reports** repository

1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (Python 3.7 version)

1. Import environment
    1. MacOS: `$ conda env create -f environment_mac.yml`
    1. Windows: `$ conda env create -f environment_win.yml`

1. Run:
    1. `$ conda activate quiz_reports_env`
    1. `$ jupyter notebook`
    1. Select **Kernal** > **Restart & Run All**