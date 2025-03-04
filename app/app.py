from flask import redirect, render_template, request, session, url_for

from app import create_app, db
from app.database import User
from app.environment import PORT
from app.forms import (
    LoginForm,
    PortfolioGenerationForm,
    PortfolioReviewForm,
    SignupForm,
    VerifyForm,
)
from app.utils import generate_otp, get_llm_response, verify_otp

app = create_app()


@app.get("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        full_name = signup_form.full_name.data
        email = signup_form.email.data
        otp = generate_otp()

        user = User.query.filter_by(email=email).first()
        if user:
            print("User already exists")
        else:
            session["full_name"] = full_name
            session["email"] = email
            session["otp"] = otp
            session["is_signup"] = True

            print("OTP:", otp)
            return redirect(url_for("verify"))

    return render_template("signup.html", signup_form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data

        user = User.query.filter_by(email=email).first()
        if user:
            otp = generate_otp()
            session["email"] = email
            session["otp"] = otp

            print("OTP:", otp)
            return redirect(url_for("verify"))
        else:
            print("User not found")

    return render_template("login.html", login_form=login_form)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "otp" not in session:
        return redirect(url_for("signup"))

    verify_form = VerifyForm()
    if verify_form.validate_on_submit():
        otp = verify_form.otp.data
        if verify_otp(otp):
            del session["otp"]

            if session["is_signup"]:
                user = User(email=session["email"], full_name=session["full_name"])
                db.session.add(user)
                db.session.commit()

            return redirect(url_for("dashboard"))
        else:
            print("Invalid OTP")

    return render_template(
        "verify.html",
        email=session.get("email"),
        verify_form=verify_form,
    )


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    full_name = session.get("full_name")
    email = session.get("email")

    portfolio_generation_form = PortfolioGenerationForm()
    portfolio_review_form = PortfolioReviewForm()

    if portfolio_generation_form.validate_on_submit():
        print(get_llm_response(form=portfolio_generation_form))
        return redirect(url_for("dashboard"))

    if portfolio_review_form.validate_on_submit():
        print(get_llm_response(form=portfolio_review_form))
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


@app.get("/logout")
def logout():
    session.clear()
    redirect(url_for("signup"))


if __name__ == "__main__":
    app.run(debug=True, port=PORT, host="0.0.0.0")
