import requests
from flask import Blueprint, flash, redirect, render_template, url_for

from paralympics.charts import bar_chart, line_chart, scatter_map
from paralympics.forms import NewQuestionForm, ParalympicsTypeForm, QuizForm, TrendSelectForm

API_BASE_URL = "http://127.0.0.1:8000"

bp = Blueprint('main', __name__)


def _get_number_questions():
    """ Helper to get the number of questions available"""
    q_resp = requests.get(f"{API_BASE_URL}/question", timeout=2)
    q_resp.raise_for_status()
    questions = q_resp.json()
    return len(questions)


def _get_question(qid):
    """ Helper to get the question"""
    q_resp = requests.get(f"{API_BASE_URL}/question/{qid}", timeout=2)
    q_resp.raise_for_status()
    q = q_resp.json()
    return q


def _get_responses(qid):
    """ Helper to get the questions and responses for a given question id"""
    r_resp = requests.get(f"{API_BASE_URL}/response/search?question_id={qid}", timeout=2)
    r_resp.raise_for_status()
    r = r_resp.json()
    return r


@bp.route("/", methods=["GET", "POST"])
@bp.route("/<int:qid>", methods=["GET", "POST"])
def index(qid=1):
    """ Page that displays one question at a time

    If user visits '/', qid defaults to 1. If user visits '/3', qid=3.

    Quiz flow:
    - Correct -> go to next question
    - Incorrect -> stay on current question
    - After last question answered correctly -> completion message, back to start
    """

    # Create an instance of the form
    form = QuizForm()

    # Logic to handle which question the user is on
    number_questions = _get_number_questions()

    if qid < 1 or qid > number_questions:
        flash("Oops, that question does not exist!")
        return redirect(url_for("main.index"))

    # Get the question and responses for the current question
    question = _get_question(qid)
    responses = _get_responses(qid)

    # Populate form (choices must be set before validate_on_submit)
    form.question.label.text = question["question_text"]
    form.question.choices = [(r["id"], r["response_text"]) for r in responses]

    if form.validate_on_submit():
        # Logic to check if the response is correct
        selected_id = form.question.data
        selected_resp = next((r for r in responses if r.get("id") == selected_id), None)
        is_correct = bool(selected_resp and selected_resp.get("is_correct"))
        if is_correct:
            # If last question, complete; else advance to the next question
            if qid == number_questions:
                flash("Well done! You completed the questions!", "success")
                return redirect(url_for("main.index", qid=1))
            else:
                return redirect(url_for("main.index", qid=qid + 1))
        else:
            # Stay on the same question
            flash("Try again!", "warning")
            return redirect(url_for("main.index", qid=qid))

    return render_template("index.html", form=form, qid=qid)


@bp.route('/question', methods=['GET', 'POST'])
def add_question():
    """ Adds a new question with 4 potential responses to the database """
    form = NewQuestionForm()
    if form.validate_on_submit():
        # Get the question text from the form
        question_text = form.question_text.data
        # Create JSON (match the database table fields)
        question = {"question_text": question_text}
        try:
            # Use POST request with the JSON
            resp = requests.post(f"{API_BASE_URL}/question", json=question)
            resp.raise_for_status()
            # The request if successful will include the new row id in the response
            qid = resp.json().get("id")
            # Get the values for the 4 possible responses from the form
            for i in range(1, 5):
                text_field = getattr(form, f"option_text_{i}")
                correct_field = getattr(form, f"is_correct_{i}")
                # Create the JSON for a response (match the fields im the database response table)
                response = {"response_text": text_field.data,
                            "is_correct": bool(correct_field.data),
                            "question_id": qid}
                # Use HTTP post request to save to the database im the response table
                resp = requests.post(f"{API_BASE_URL}/response", json=response)
                resp.raise_for_status()
            flash(f"Question saved!", "success")
        except requests.RequestException as e:
            flash(f"Failed to add question: {e}", "danger")

    return render_template("new_question.html", form=form)


@bp.route('/locations')
def locations():
    """ Generates the page that displays a map showing where the Paralympics have been held """
    fig = scatter_map()
    fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}
    return render_template('locations.html', fig_html=fig_for_jinja)


@bp.route('/participants', methods=['GET', 'POST'])
def participants():
    form = ParalympicsTypeForm()
    if form.validate_on_submit():
        # Get the list of selected options from the form data
        paralympics_types = form.paralympics_types.data
        figs = []
        for p_type in paralympics_types:
            fig = bar_chart(p_type)
            fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}
            figs.append(fig_for_jinja)
        return render_template('participants.html', figs=figs, form=form)

    # If the page is a GET request, or there is a form error, then return the page without charts
    return render_template('participants.html', form=form)


@bp.route('/trends', methods=['GET', 'POST'])
def trends():
    """ Generates the page that displays trends

    Gets the selection option value from a select in a form on the trends.html page
    Defaults to 'countries' otherwise
    Uses the value name to pass to the line_chart() function
    Generate a form of the chart with the necessary Plotly JavaScript elements
    Pass the form and the chart code to the template to generate the page

    """
    form = TrendSelectForm()
    if form.validate_on_submit():
        selected_type = form.selected_type.data
    else:
        selected_type = "countries"  # Default if no choice made
    fig = line_chart(selected_type)
    fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}
    return render_template('trends.html', fig_html=fig_for_jinja, form=form)


@bp.get('/news')
def news():
    """ Generates the page that displays hacker news via algolia which allows for keyword search """
    endpoint = 'https://hn.algolia.com/api/v1/search?query=paralympics&tags=story'
    resp = requests.get(endpoint)
    resp.raise_for_status()
    data = resp.json()
    stories = []
    for hit in data.get('hits', [])[:20]:
        title = hit.get('title') or '(no title)'
        url = hit.get('url') or hit.get('story_url') or '(no url)'
        stories.append({'title': title, 'url': url})
    return render_template('news.html', stories=stories)
