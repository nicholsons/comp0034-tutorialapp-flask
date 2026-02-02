from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, SelectField, SelectMultipleField, StringField, \
    SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import CheckboxInput, ListWidget


class NewQuestionForm(FlaskForm):
    """ A new question with options """
    question_text = StringField("Question text", validators=[DataRequired()])
    option_text_1 = StringField("Option 1 text", validators=[DataRequired()])
    is_correct_1 = BooleanField("Correct answer?", render_kw={"class": "form-check-input"})
    option_text_2 = StringField("Option 2 text", validators=[DataRequired()])
    is_correct_2 = BooleanField("Correct answer?", render_kw={"class": "form-check-input"})
    option_text_3 = StringField("Option 3 text", validators=[DataRequired()])
    is_correct_3 = BooleanField("Correct answer?", render_kw={"class": "form-check-input"})
    option_text_4 = StringField("Option 4 text", validators=[DataRequired()])
    is_correct_4 = BooleanField("Correct answer?", render_kw={"class": "form-check-input"})
    submit = SubmitField("Save new question", render_kw={"class": "btn btn-primary"})

    def validate(self, extra_validators=None):
        # Run field validators first (and forward any extra validators)
        valid = super().validate(extra_validators=extra_validators)
        if not valid:
            return False

        correct_flags = [
            self.is_correct_1.data,
            self.is_correct_2.data,
            self.is_correct_3.data,
            self.is_correct_4.data,
        ]
        correct_count = sum(bool(x) for x in correct_flags)

        if correct_count != 1:
            msg = "Select exactly one correct answer."
            # Attach to all checkboxes so the error is visible next to them
            for f in (self.is_correct_1, self.is_correct_2, self.is_correct_3, self.is_correct_4):
                f.errors.append(msg)
            return False

        return True


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
