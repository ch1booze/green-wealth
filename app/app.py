from flask import redirect, render_template, request, session, url_for

from app import create_app, db
from app.forms import (
    LoginForm,
    PortfolioGenerationForm,
    PortfolioReviewForm,
    SignupForm,
    VerifyForm,
)
from app.utils import generate_otp

app = create_app()

with app.app_context():
    db.create_all()


@app.get("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        otp = generate_otp()

        session["full_name"] = full_name
        session["email"] = email
        session["otp"] = otp

        print("OTP:", otp)
        return redirect(url_for("verify"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        otp = generate_otp()

        session["email"] = email
        session["otp"] = otp

        print("OTP:", otp)
        return redirect(url_for("verify"))

    return render_template("login.html", form=form)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "otp" not in session:
        return redirect(url_for("signup"))

    form = VerifyForm()
    if form.validate_on_submit():
        otp = form.otp.data
        if otp == session["otp"]:
            del session["otp"]
            return redirect(url_for("dashboard"))

    return render_template("verify.html", email=session.get("email"), form=form)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    full_name = session.get("full_name")
    email = session.get("email")

    portfolio_generation_form = PortfolioGenerationForm()
    portfolio_review_form = PortfolioReviewForm()

    if portfolio_generation_form.validate_on_submit() and "submit" in request.form:
        session["portfolio"] = {
            "age": portfolio_generation_form.age.data,
            "risk_level": portfolio_generation_form.risk_level.data,
            "investment_horizon": portfolio_generation_form.investment_horizon.data,
            "monthly_investment": portfolio_generation_form.monthly_investment.data,
            "investment_goal": portfolio_generation_form.investment_goal.data,
        }
        return redirect(url_for("dashboard"))

    if portfolio_review_form.validate_on_submit() and "submit" in request.form:
        session["review_portfolio"] = {
            "age": portfolio_review_form.age.data,
            "risk_level": portfolio_review_form.risk_level.data,
            "investment_horizon": portfolio_review_form.investment_horizon.data,
            "funds": [
                {"fund_name": fund.fund_name.data, "amount": fund.amount.data}
                for fund in portfolio_review_form.funds.entries
            ],
        }
        return redirect(url_for("dashboard"))

    if "add_fund" in request.form:
        portfolio_review_form.funds.append_entry()

    for idx, fund in enumerate(portfolio_review_form.funds.entries):
        if f"funds-{idx}-remove" in request.form:
            portfolio_review_form.funds.pop_entry()
            return redirect(url_for("dashboard"))

    return render_template(
        "dashboard.html",
        full_name=full_name,
        email=email,
        portfolio_generation_form=portfolio_generation_form,
        portfolio_review_form=portfolio_review_form,
    )


if __name__ == "__main__":
    app.run(debug=True)
