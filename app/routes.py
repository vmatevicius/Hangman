import random
from operator import itemgetter

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from app import app, bcrypt, db
from app.db_operations import DBoperations
from app.forms.forms import LoginForm, RegistrationForm
from app.utils import Utilities

utils = Utilities()
db_operations = DBoperations()


@app.route("/", methods=["GET"])
def index():
    return render_template("landing_page.html")


@app.route("/home", methods=["GET"])
@login_required
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    db.create_all
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_operations.get_account_by_username(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("home"))
            else:
                flash("Login failed, wrong password ", "danger")
        else:
            flash("Login failed, user does not exist", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register_user():
    db.create_all
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.args.get('type') != None:
            profile_picture = f"/static/profile_pictures/{request.args.get('type').strip()}.jpg"
        else:
            profile_picture = "/static/default.png"
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        account = db_operations.create_account(
            form.username.data,
            form.name.data,
            form.surname.data,
            hashed_password,
            form.email.data,
            profile_picture
        )
        login_user(account)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/profile_picture", methods=["GET"])
def profile_picture():
    return render_template("profile_picture.html")

@app.route("/account", methods=["GET"])
@login_required
def account():
    user = db_operations.get_account(current_user.get_id())
    transactions = db_operations.get_user_transactions(user)
    return render_template("account.html", user=user, transactions=transactions)

@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    user = db_operations.get_account(current_user.get_id())
    if request.method == "GET":
        return render_template("shop.html", user=user)
    else:
        amount = request.form["buy"]
        price = int(amount) * 30
        if price <= user.credits:
            transaction = db_operations.create_transaction(user, price, int(amount))
            db_operations.update_account_after_purchase(account=user, tickets=transaction.tickets, credits=transaction.price)
        else:
            flash(f"Not enough credits", "danger")
            return redirect("/shop")
    return render_template("shop.html", user=user)

@app.route("/gamble", methods=["GET", "POST"])
def gamble():
    
    user = db_operations.get_account(current_user.get_id())
    if request.method == "GET":
        return render_template("gamble.html")
    random_number = random.randint(1, 6)
    bet = request.form["bet"]
    guessed_number = request.form["guessed_number"]
    if int(bet) > user.credits:
        flash(f"Not enough credits", "danger")
        return redirect("/gamble")
    if random_number != int(guessed_number):
        flash(f"Wrong guess", "danger")
        flash(f"the number was - {random_number}", "danger")
        db_operations.remove_credits(account=user, credits=int(bet))
        return redirect("/gamble")
    
    if random_number == int(guessed_number):
        flash(f"You won {int(bet) * 1.5} credits!", "success")
        db_operations.add_credits(account=user, credits=int(bet) * 1.5)
        return redirect("/gamble")

    
    return render_template("gamble.html")

@app.route("/leaderboards", methods=["GET"])
def leaderboards():
    accounts = db_operations.get_all_accounts()
    unsorted_user_score_data = db_operations.retrieve_accounts_game_data(accounts)
    sorted_user_data = sorted(
        unsorted_user_score_data, key=itemgetter("score"), reverse=True
    )
    return render_template("leaderboards.html", sorted_user_data=sorted_user_data)


@app.route("/difficulties", methods=["GET"])
@login_required
def difficulties():
    return render_template("difficulties.html")


@app.route("/easy", methods=["GET"])
@login_required
def easy():
    user = db_operations.get_account(current_user.get_id())
    return utils.launch_game(tries=7, difficulty="easy", user=user)


@app.route("/add_letter_easy", methods=["POST"])
@login_required
def add_letter_easy():
    user = db_operations.get_account(current_user.get_id())
    return utils.add_letter(difficulty="easy", user=user, points= 10)

@app.route("/reveal_letter_easy", methods=["POST"])
@login_required
def reveal_letter_easy():
    user = db_operations.get_account(current_user.get_id())
    return utils.reveal_letter(difficulty="easy", user=user, points= 10)

@app.route("/medium", methods=["GET"])
@login_required
def medium():
    user = db_operations.get_account(current_user.get_id())
    return utils.launch_game(tries=5, difficulty="medium", user=user)


@app.route("/add_letter_medium", methods=["POST"])
@login_required
def add_letter_medium():
    user = db_operations.get_account(current_user.get_id())
    return utils.add_letter(difficulty="medium", user=user, points= 20)

@app.route("/reveal_letter_medium", methods=["POST"])
@login_required
def reveal_letter_medium():
    user = db_operations.get_account(current_user.get_id())
    return utils.reveal_letter(difficulty="medium", user=user, points= 20)

@app.route("/hard", methods=["GET"])
@login_required
def hard():
    user = db_operations.get_account(current_user.get_id())
    return utils.launch_game(tries=3, difficulty="hard", user=user)


@app.route("/add_letter_hard", methods=["POST"])
@login_required
def add_letter_hard():
    user = db_operations.get_account(current_user.get_id())
    return utils.add_letter(difficulty="hard", user=user,points= 30)

@app.route("/reveal_letter_hard", methods=["POST"])
@login_required
def reveal_letter_hard():
    user = db_operations.get_account(current_user.get_id())
    return utils.reveal_letter(difficulty="hard", user=user, points= 30)


@app.route("/defeat")
@login_required
def game_lost_landing():
    return render_template("defeat.html")


@app.route("/victory")
@login_required
def game_won_landing():
    return render_template("victory.html")


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
