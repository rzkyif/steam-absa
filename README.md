# steam-absa
A web application for information retrieval, aspect extraction, and aspect-based sentiment analysis on Steam review data of multiple games.

## Requirements

- Python 3
- Node.js
- [PNPM](https://pnpm.io/installation#using-corepack)

## Setup

### Backend (be)

1. Enter the backend directory

        cd be

2. Setup virtual environment

        python -m venv .venv

3. Activate virtual environment

    On Windows:

        . .venv/Scripts/activate

    On Linux:

        . .venv/bin/activate

4. Install requirements

        pip install hug waitress nltk spacy pandas numpy

5. Install spaCy model 

        python -m spacy download en_core_web_sm

6. (Optional) Set Visual Studio Code interpreter for development

    In the editor, when opening a Python file, set the interpreter to the virtual environment one by clicking the Python version number on the bottom right, selecting `Enter interpreter path...` and locating the Python interpreter at `./be/.venv/bin/python3`.

7. Start backend server

    Development w/ Hot Reload:

        hug -f main.py

    Production:

        waitress-serve --port=8000 main:__hug_wsgi__

### Frontend (fe)

1. Enter the frontend directory

        cd fe

2. Install Node.js dependencies with PNPM

        pnpm install

3. Start frontend server

    Development w/ Hot Reload:

        pnpm dev

    Production:

        pnpm start