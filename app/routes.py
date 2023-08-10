from app import db, app, bcrypt
from app.models.account_model import Account
import forms.forms as forms
import utils
import db_operations
from operator import itemgetter
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required

EASY_MODE_POINTS = 10
MEDIUM_MODE_POINTS = 20
HARD_MODE_POINTS = 30


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
    form = forms.LoginForm()
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
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        account = db_operations.create_account(
            form.username.data,
            form.name.data,
            form.surname.data,
            hashed_password,
            form.email.data,
        )
        login_user(account)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/account", methods=["GET"])
@login_required
def account():
    user = db_operations.get_account(current_user.get_id())
    return render_template("account.html", user=user)


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
    global good_guesses
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global usable_letters

    good_guesses = 0
    wrong_guesses = 0

    usable_letters = "abcdefghijklmnopqrstuvwxyz"
    animal_type = utils.get_random_animal_type()
    word_to_guess = utils.get_random_animal(utils.get_animals(animal_type))
    tries = 7
    wrong_letters = []
    empty_spots = len(word_to_guess)
    visuals = utils.create_game_board(len(word_to_guess))
    image = utils.get_easy_image_path(tries)

    return render_template(
        "easy.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/add_letter_easy", methods=["POST"])
@login_required
def add_letter_easy():
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global good_guesses
    global usable_letters

    guess = request.form["letter"]
    usable_letters = usable_letters.replace(guess, "")
    succeeded = False
    for index, letter in enumerate(word_to_guess):
        if letter == guess:
            good_guesses += 1
            succeeded = True
            visuals[index] = letter
            empty_spots -= 1
    if succeeded == False:
        wrong_letters.append(guess)
        wrong_guesses += 1
        tries -= 1
        if tries == 0:
            user = db_operations.get_account(current_user.get_id())
            db_operations.update_account_after_lost_game(
                user, good_guesses, wrong_guesses
            )
            flash(f"Secret word was - {word_to_guess}", "danger")
            return redirect("/defeat")

    if empty_spots == 0:
        user = db_operations.get_account(current_user.get_id())
        db_operations.update_account_after_won_game(
            user, good_guesses, wrong_guesses, EASY_MODE_POINTS
        )
        flash(f"Secret word was - {word_to_guess}", "danger")
        return redirect("/victory")

    image = utils.get_easy_image_path(tries)

    return render_template(
        "easy.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/medium", methods=["GET"])
@login_required
def medium():
    global good_guesses
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global usable_letters

    good_guesses = 0
    wrong_guesses = 0

    usable_letters = "abcdefghijklmnopqrstuvwxyz"
    animal_type = utils.get_random_animal_type()
    word_to_guess = utils.get_random_animal(utils.get_animals(animal_type))
    tries = 5
    wrong_letters = []
    empty_spots = len(word_to_guess)
    visuals = utils.create_game_board(len(word_to_guess))
    image = utils.get_medium_image_path(tries)

    return render_template(
        "medium.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/add_letter_medium", methods=["POST"])
@login_required
def add_letter_medium():
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global good_guesses
    global usable_letters

    guess = request.form["letter"]
    usable_letters = usable_letters.replace(guess, "")
    succeeded = False
    for index, letter in enumerate(word_to_guess):
        if letter == guess:
            good_guesses += 1
            succeeded = True
            visuals[index] = letter
            empty_spots -= 1
    if succeeded == False:
        wrong_letters.append(guess)
        wrong_guesses += 1
        tries -= 1
        if tries == 0:
            user = db_operations.get_account(current_user.get_id())
            db_operations.update_account_after_lost_game(
                user, good_guesses, wrong_guesses
            )
            flash(f"Secret word was - {word_to_guess}", "danger")
            return redirect("/defeat")

    if empty_spots == 0:
        user = db_operations.get_account(current_user.get_id())
        db_operations.update_account_after_won_game(
            user, good_guesses, wrong_guesses, MEDIUM_MODE_POINTS
        )
        flash(f"Secret word was - {word_to_guess}", "danger")
        return redirect("/victory")

    image = utils.get_medium_image_path(tries)

    return render_template(
        "medium.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/hard", methods=["GET"])
@login_required
def hard():
    global good_guesses
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global usable_letters

    good_guesses = 0
    wrong_guesses = 0

    usable_letters = "abcdefghijklmnopqrstuvwxyz"
    animal_type = utils.get_random_animal_type()
    word_to_guess = utils.get_random_animal(utils.get_animals(animal_type))
    tries = 3
    wrong_letters = []
    empty_spots = len(word_to_guess)
    visuals = utils.create_game_board(len(word_to_guess))
    image = utils.get_hard_image_path(tries)

    return render_template(
        "hard.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/add_letter_hard", methods=["POST"])
@login_required
def add_letter_hard():
    global wrong_guesses
    global word_to_guess
    global tries
    global wrong_letters
    global empty_spots
    global visuals
    global animal_type
    global good_guesses
    global usable_letters

    guess = request.form["letter"]
    usable_letters = usable_letters.replace(guess, "")
    succeeded = False
    for index, letter in enumerate(word_to_guess):
        if letter == guess:
            good_guesses += 1
            succeeded = True
            visuals[index] = letter
            empty_spots -= 1
    if succeeded == False:
        wrong_letters.append(guess)
        wrong_guesses += 1
        tries -= 1
        if tries == 0:
            user = db_operations.get_account(current_user.get_id())
            db_operations.update_account_after_lost_game(
                user, good_guesses, wrong_guesses
            )
            flash(f"Secret word was - {word_to_guess}", "danger")
            return redirect("/defeat")

    if empty_spots == 0:
        user = db_operations.get_account(current_user.get_id())
        db_operations.update_account_after_won_game(
            user, good_guesses, wrong_guesses, HARD_MODE_POINTS
        )
        flash(f"Secret word was - {word_to_guess}", "danger")
        return redirect("/victory")

    image = utils.get_hard_image_path(tries)

    return render_template(
        "hard.html",
        animal_type=animal_type,
        tries=tries,
        wrong_letters=wrong_letters,
        visuals=visuals,
        usable_letters=usable_letters,
        image=image,
    )


@app.route("/defeat")
@login_required
def game_lost_landing():
    return render_template("defeat.html")


@app.route("/victory")
@login_required
def game_won_landing():
    return render_template("victory.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
