from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import CheckboxInput, ListWidget


class QuizForm(FlaskForm):
    """ A form with 1 question as a radio field """
    question = RadioField("",
                          choices=[],
                          coerce=int,
                          validators=[DataRequired()],
                          )
    submit = SubmitField("Submit response", render_kw={"class": "btn btn-primary"})


class TrendSelectForm(FlaskForm):
    selected_type = SelectField("Select the data to show in the chart",
                                choices=[('countries', 'Countries'), ('events', 'Events'),
                                         ('participants', 'Participants'), ('sports', 'Sports')],
                                default="countries",
                                validators=[DataRequired()],
                                render_kw={"class": "form-select",
                                           "aria-label": "Select the data to show in the chart",
                                           "onchange": "this.form.submit()"},

                                )


class ParalympicsTypeForm(FlaskForm):
    paralympics_types = SelectMultipleField(
        "Select one or both types of Paralympics",
        choices=[("winter", "Winter"), ("summer", "Summer")],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False),
        validators=[Length(min=1, message="Select at least one.")],
    )
    submit = SubmitField("Generate selected charts")
