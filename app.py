import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, randlist

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure name was submitted
        elif not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must fill re-enter password field", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password field and re-enter password field are not the same", 400)

        # Ensure username is unique
        usernames = db.execute("SELECT username FROM users;")
        name = request.form.get("username")
        for row in usernames:
            if row["username"] == name:
                return apology("username already taken", 400)

        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (name, username, hash) VALUES (?, ?, ?);", name, username, generate_password_hash(password))

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Allow users to change their passwords"""

    if request.method == "POST":
        if not request.form.get("password") or not request.form.get("new_password") or not request.form.get("confirm_password"):
            return apology("must fill all boxes", 403)
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid password", 403)
        elif request.form.get("new_password") != request.form.get("confirm_password"):
            return apology("password field and re-enter password field are not the same", 403)
        new_password = request.form.get("new_password")

        db.execute("UPDATE users SET hash = ? WHERE id = ?;", generate_password_hash(new_password), user_id)

        return redirect("/")
    else:
        return render_template("password.html")



@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    user_id = session["user_id"]
    username = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]['username']
    name = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]['name']


    if request.method == "GET":
        checker = 0
        quiz = int (db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]['quiz'])
        if quiz == 0:
            questions = db.execute("SELECT question FROM samples;")

            for i in range(29):
                questions[i]["question"] = questions[i]["question"].replace("CreativeReaper", name)

            c_answers = db.execute("SELECT c_answer FROM samples;")
            w_answer1 = db.execute("SELECT w_answer1 FROM samples;")
            w_answer2 = db.execute("SELECT w_answer2 FROM samples;")

            numlist = randlist(28)

            samples = db.execute("SELECT * FROM samples;")
            return render_template("quiz.html", numlist=numlist, samples=samples, checker=checker, questions=questions)
        else:
            questions = db.execute("SELECT question FROM samples;")
            samples = db.execute("SELECT * FROM samples;")
            checker = 1
            answers = db.execute("SELECT * FROM answers WHERE user_id = ?;", user_id)
            numlist = randlist(28)
            return render_template("quiz.html", answers=answers, samples=samples, numlist=numlist, questions=questions)

    else:

        if int (db.execute("SELECT quiz FROM users WHERE id = ?", user_id)[0]['quiz']) == 0:
            for i in range(10):
                question = request.form.get("question" + str(i+1))
                c_answer = request.form.get(str(i+1) + "c_answer")
                w_answer1 = request.form.get(str(i+1) + "w_answer1")
                w_answer2 = request.form.get(str(i+1) + "w_answer2")
                q_no = i+1

                db.execute("INSERT INTO answers (user_id, username, name, question_no, question, c_answer, w_answer1, w_answer2) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", user_id, username, name, q_no, question, c_answer, w_answer1, w_answer2)
                db.execute("UPDATE users SET quiz = '1' WHERE id = ?;", user_id)
        else:
            for i in range(10):
                question = request.form.get("question" + str(i+1))
                c_answer = request.form.get(str(i+1) + "c_answer")
                w_answer1 = request.form.get(str(i+1) + "w_answer1")
                w_answer2 = request.form.get(str(i+1) + "w_answer2")
                q_no = i+1

                db.execute("UPDATE answers SET question = ?, c_answer = ?, w_answer1 = ?, w_answer2 = ? WHERE user_id = ? AND question_no = ?;", question, c_answer, w_answer1, w_answer2, user_id, q_no)

        url = f"https://actualreaper-didactic-parakeet-5gqg5gv6v65wfv4w5-5000.app.github.dev/test?url={username}"
        return render_template("confirmation.html", url=url)

@app.route("/test", methods=["GET", "POST"])

def test():

    if request.method == "GET":

        user_id = session["user_id"]
        username = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]['username']
        users_db = db.execute("SELECT * FROM users;")
        questions_db = db.execute("SELECT * FROM answers;")

        usernames = []
        for row in users_db:
            usernames.append(row["username"])

        global name
        name = request.args.get("url")
        if not name or name not in usernames:
            return apology("Invalid Link")

        questions = []
        c_answer = []
        w_answer1 = []
        w_answer2 = []

        for row in questions_db:
            if row["username"] == name:
                questions.append(row["question"])
                c_answer.append(row["c_answer"])
                w_answer1.append(row["w_answer1"])
                w_answer2.append(row["w_answer2"])


        answers = []
        fullRandomAnsList = []
        for i in range(10):
            ansList = [c_answer[i], w_answer1[i], w_answer2[i]]
            randomAnsList = []
            j = 0
            while(j < 3):
                randomChoice = random.choice(ansList)
                if not randomChoice in randomAnsList:
                    randomAnsList.append(randomChoice)
                    j += 1
            fullRandomAnsList.append(randomAnsList)



        return render_template("test.html", questions=questions, c_answers=c_answer, w_answer1=w_answer1, w_answer2=w_answer2, questions_db=questions_db, ansList=fullRandomAnsList, name=name)

    elif request.method == "POST":

        name = request.form.get("urlName")

        actualName = db.execute("SELECT name FROM users WHERE username = ?", name)[0]["name"]

        c_answer = []
        questions = []
        answers = db.execute("SELECT * FROM answers WHERE username = ?;", name)

        for i in range(10):
            c_answer.append(answers[i]["c_answer"])
            questions.append(answers[i]["question"])

        a1 = request.form.get("answer1")
        a2 = request.form.get("answer2")
        a3 = request.form.get("answer3")
        a4 = request.form.get("answer4")
        a5 = request.form.get("answer5")
        a6 = request.form.get("answer6")
        a7 = request.form.get("answer7")
        a8 = request.form.get("answer8")
        a9 = request.form.get("answer9")
        a10 = request.form.get("answer10")

        answer_list = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]
        for answer in answer_list:
            if not answer:
                return apology("Please fill all Answers")

        wAns = []
        cAns = []
        qNo = []
        checker = []


        testNumbers = 0
        for i in range(10):
            if c_answer[i] == answer_list[i]:
                testNumbers += 1
            else:
                wAns.append(answer_list[i])
                qNo.append(i)
                checker.append(i+1)

        w_questions = []

        for num in qNo:
            w_questions.append(questions[num])
            cAns.append(c_answer[num])

        return render_template("result.html", numbers=testNumbers, wAns=wAns, w_questions=w_questions, cAns=cAns, length=len(qNo), name=actualName)



