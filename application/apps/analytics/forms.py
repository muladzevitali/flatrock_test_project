__author__ = "Vitali Muladze"

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class ReportDateForm(FlaskForm):
    """Year choosing form for reports"""
    years = SelectField("Select Year", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ReportDateForm, self).__init__(*args, **kwargs)
        years = [(str(year), str(year)) for year in range(2012, 2018)]
        years += [("all", "Full Report")]
        self.years.choices = years


class ForecastDateForm(FlaskForm):
    """Year choosing form for Prediction"""
    years = SelectField("Select years", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ForecastDateForm, self).__init__(*args, **kwargs)
        years = [(str(year), str(year)) for year in range(2018, 2029)]
        years += [("all", "Full Forecast")]
        self.years.choices = years
