from flask import Blueprint, render_template

from paralympics.charts import bar_chart, line_chart, scatter_map
from paralympics.forms import TrendSelectForm, ParalympicsTypeForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


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
