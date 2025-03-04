from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    EmailField,
    FieldList,
    FormField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Log In")


class VerifyForm(FlaskForm):
    otp = StringField("OTP", validators=[DataRequired()])
    submit = SubmitField("Verify")


class PersonalInfoForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired()])
    risk_level = SelectField(
        "Risk Level",
        choices=[
            ("aggressive", "Aggressive"),
            ("moderate", "Moderate"),
            ("conservative", "Conservative"),
        ],
        validators=[DataRequired()],
    )
    investment_horizon = SelectField(
        "Investment Horizon",
        choices=[
            ("short_term", "Short-Term (0-3 years)"),
            ("medium_term", "Medium-Term (3-7 years)"),
            ("long_term", "Long-Term (7+ years)"),
        ],
        validators=[DataRequired()],
    )


class FundForm(FlaskForm):
    fund_name = StringField("Fund Name", validators=[DataRequired()])
    amount = DecimalField("Amount ($)", validators=[DataRequired()])
    remove = SubmitField("Remove")


class PortfolioGenerationForm(PersonalInfoForm):
    monthly_investment = DecimalField(
        "Monthly Investment ($)",
        validators=[DataRequired()],
    )
    investment_goal = SelectField(
        "Investment Goal",
        choices=[
            ("random", "Random Investing Portfolio"),
            ("emergency", "Emergency Funds (12 months)"),
            ("freedom", "Financial Freedom"),
            ("house", "Saving for House Downpayment"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Generate Portfolio")


class PortfolioReviewForm(PersonalInfoForm):
    funds = FieldList(FormField(FundForm), min_entries=1)
    add_fund = SubmitField("Add Fund")
    submit = SubmitField("Review Portfolio")
