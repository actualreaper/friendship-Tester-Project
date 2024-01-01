# Friendship Tester
## Video Demo:  https://youtu.be/NtG7FaHwzW4
### Description:
My project is a web application that creates ten multiple choice questions with the help of the user. After the test is created the user gets a link to play the test. After following the link, you can play the test. After completing the test you get the result and all the questions you got wrong with correct answers.
### App Understanding:
Here are all the files that I created to make this project with their details:
### Project.db:
Project.db is the database file that I created to store this website's data. It consists of three tables: Users, Samples, and answers.
* **Users:** This table stores all of the user's account's data.
    * **id:** Every user is given a unique ID which is also the primary key.
    * **name:** This column stores the name of the user.
    * **username:** This column stores the username of the user.
    * **hash:** This column stores the password's hash of the user.
    * **quiz:** This column stores a numeric value. If it is 0 then it means that the user has not create a quiz yet. If it is 1 then it means the the user has made a quiz.
    * Here are the lines of SQL code that I wrote to make this table:
    ```
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    quiz CHAR NOT NULL DEFAULT 0);
    ```
* **Samples:** This table stores some sample questions and answers so when a user is creating a quiz, he can see some sample questions that he can edit.
    * **ID:** This column stores the unique IDs of the sample questions.
    * **Question:** This column stores the samples questions.
    * **C_answer:** This column stores the correct answers of the sample questions.
    * **W_answer1:** This column stores the first wrong answer of the sample questions.
    * **W_answer2:** This column stores the second wrong answer of the sample questions.
    * Here are the lines of SQL code that I wrote to create this table:
    ```CREATE TABLE answers (
    CREATE TABLE samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    question TEXT NOT NULL,
    c_answer TEXT NOT NULL,
    w_answer1 TEXT NOT NULL,
    w_answer2 TEXT NOT NULL);
    ```
* **Answers:** This table stores all of the questions and their answers of all the users who have made a quiz.
    * **ID:** This column stores the unique ID of the questions.
    * **User_ID:** This column stores the IDs of the users who created the quiz.
    * **Username:** This column stores the usernames of the users who created the quiz.
    * **Name:** This column stores the name of the users who created the quiz.
    * **Question_no:** This column stores the question numbers of the questions of the quiz that the user created. It resets after every ten questions because a user can only create ten questions in a quiz.
    * **Question:** This column stores the questions of every quiz created.
    * **C_answer:** This column stores the correct answers of every question of every quiz created.
    * **W_answer1:** This column stores the first wrong answer of every question of every quiz created.
    * **W_answer2:** This column stores the second wrong answer of every question of every quiz created.
    * Here are the lines of SQL code that I wrote to create this table:
    ```
    CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    question_no INTEGER NOT NULL,
    question TEXT NOT NULL,
    c_answer TEXT NOT NULL,
    w_answer1 TEXT NOT NULL,
    w_answer2 TEXT NOT NULL);
    ```
### app.py:
Atop the file are a bunch of imports, among them CS50’s SQL module and a few helper functions. More on those soon. After configuring Flask, this file disables caching of responses. It then further configures Flask to store sessions on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask’s default. The file then configures CS50’s SQL module to use project.db. After that are a whole bunch of routes.
* **index:** There is nothing too special going on in this route. All it does is that it returns the main page (index.html).
* **login:** This route is used to login to this website. It accepts both request methods (GET and POST). First it forgets if any user is currently logged in using session.clear() method from flask library. After that, if the requested method is GET, it just returns the login.html template, If the requested method is POST then first it checks if all of the input fields were filled (ie. Username and Password). Then it checks if the username exists and if the password that the user input is correct by querying the **project.db** database and then it redirects the user to the homepage (index.html).
* **register:** This route is used to create an account on this website. It accepts both request methods (GET and POST). First it forgets if any user is currently logged in using session.clear() method from flask library. After that, if the requested method is GET, it just returns the register.html template. If the requested method is POST then first it checks if all of the input fields were filled (ie. Name, Username, Password, and Confirm Password). Then it checks if the username that the user input was unique by checking all of the usernames in **project.db** database. After that it stores the name, username and password hash in the **project.db** database. By doing all this, this route creates a new account.
* **logout:** This route logs out a user by using the session.clear() method from flask library.
* **password:** This route allows a user to change their account's password. It accepts both request methods (ie. GET and POST). If the requested method is GET, it just returns the password.html template. If the requested method is POST then first it checks if all of the input fields were filled (ie. Password, New Password, and Confirm New Password). After that it generates the new password's hash and saves it in the **project.db** database. After that it redirects the user to the homepage (index.html).
* **quiz:** This route accepts both request methods. First it takes the username and name into memory from the **project.db** database. Then it checks if the requested method is GET OR POST. If the requested method is GET then it checks that if the quiz value of the user's table of **project.db** database is 0 or 1. If the value is 0 then it returns the template quiz.html and sends four lists the client side. These are those four lists:
    * **Numlist:** It is a list that contains ten random numbers from 0 to 29. It is used to display the samples questions in random order when the user is creating the quiz.
    * **Samples:** It contains everything from the samples table.
    * **Checker:** It contains a value that is either 0 or 1. If the value is 0 that means that the user have not made a quiz already and then when the he/she is creating the quiz he/she will get random sample questions. On the other hand, if the checker's value is 1, that will mean that the user has already creaded a quiz so if he/she wants to edit their quiz they can simply try to create the quiz again and the will get the questions that they set in their quiz so that he/she can edit them and save them again.
    * **Questions:** It contains all of the sample questions with the name of the user that is currently logged in. In the database the sample questions do not contain the name of the user that is creating the quiz.

If the quiz's value is 1 then it returns the template quiz.html and sends four lists the client side. Three of them are already mentioned (ie., numlist, questions, and samples). The last list is called answers and it contains all of the questions and answers that the users that is currently logged in has set while creating the test. If the requested method is POST then it means that the user has created (or edited) and submitted their quiz. So then it will save the users questions and answers in the **answers** table in **project.db** database or if the user had already created the quiz and only updated it then it will also only update the questions and answers in the table. Then it returns the template confirmation.html and sends a variable named url to the client side. The value of the url is an actual url that will show up on confirmation.html page. With that link that user can play the test.
* **test:** This route is used when the user wants to play the test. It accepts both request methods (GET and POST). If the requested method is GET then it returns the template test.html with six lists and a variable. These are the lists:
    * **questions:** It contains all ten of the questions that are taken from the answers table from the **project.db** database. These questions are displayed in random order when someone is playing the quiz.
    * **c_answers, w_answer1, w_answer2:** These three lists contain the multiple choice answers of every question. Similer to the question's list, these are also taken from the answers table from the **project.db** database.
    * **questions_db:** This is a list that contains data from the answers table from **project.db** database.
    * **ansList:** This list contains the correct answer and both wrong answers in random order. It is used to randomize the answers.
    * **name:** This is a variable that contains the name of the person whos quiz is being played.

If the requested method is POST, that would mean that the user has submitted the quiz and is awaiting the results. So in that case, it checks all the answers and and saves the result. Then it returns the result.html template which displays the result and shows all of the questions that the user got wrong along with the correct answer.

### helpers.py:
In helpers.py three functions are defined that are used in app.py.
* **apology:** This function ultimately returns a template, apology.html. In this web application, this function is used everytime the user doesn't follow the instructions. For example, if the user forgets to fill an input field, like when logging in they forget to write their username, this function is called to warn the user.
* **login_required:** This function is called when it is mandatory to login before accessing a route.
* **randlist:** This function is used to create a list of random ten integers.

### templates:
This folder contains the templates that were used to create the web application.
### static:
This folder contains the CSS that was used to create the web application.
