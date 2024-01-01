#import csv
#import datetime
#import pytz
#import requests
#import subprocess
#import urllib
#import uuid

from flask import redirect, render_template, session
from functools import wraps
from random import randint

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# def datetimeRN(user_input):
#     """Returns date and time"""

#     today = datetime.datetime.today()
#     if user_input == "day":
#         return int(today.strftime("%d"))
#     elif user_input == "month":
#         return int(today.strftime("%m"))
#     elif user_input == "year":
#         return int(today.strftime("%Y"))
#     elif user_input == "hour":
#         return int(today.strftime("%H"))
#     elif user_input == "minute":
#         return int(today.strftime("%M"))
#     elif user_input == "second":
#         return int(today.strftime("%S"))

def randlist(number):
    i = 0
    arr = []
    while i <= number:
        num = randint(0, number)
        if not num in arr:
            arr.append(num)
            i += 1
    return arr

