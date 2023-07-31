### Game requirements:

* max try count - 10
* every failed attempt - 1 try
* if 0 tries left - game over
* ability to register user
* leaderboards
* easy/medium/hard modes
* score system - easy mode - 10points for a win, medium - 20, hard - 50
* user account summary( games played, games won/lost, correct/wrong guess count, best score)

### Data requirements:

* Account table:
    must have:
    * Username
    * Name
    * Surname
    * Email adress
    * Games played count
    * games won/lost count
    * correct/wrong guess count
    * highest achieved score

### Basic requirements:

* ADD TYPE ANNOTATIONS
* ADD INFORMATION LOGGING
* CREATE TESTS


### Step 1
Setting working enviroment:

* Create github repository
* Add virtual enviroment, README.md, .gitignore, requirements.txt files.
* From main branch, create development branch
  and from development branch out to specific modules/functionalities etc.
  you are trying to create

### Step 2
Setting backend(database models,endpoints, crude operations,forms)

* Account:
    * create account database model
    * create a form for user registration/ login
    * create endpoint and add functionality to register new user
    * create endpoint and add functionality to connect new user
    * add ability to log out
    * create crude operations

### Step 3

Dockerizing

### Step 4
Making the game:

* Create login page
* Create register page
* Add log out functionality
* Create account overview page
* Create leaderboard page
* Create main page which lets you choose easy/medium/hard modes
* Create game pages for each difficulty
* Add tries count, picture of rope to hang from, place to enter letters,
  visualization of entered letters(correct/wrong)
* If the game is lost immediately, redirect to the scoreboard
* if the game is won, ask if player want's to continue, if not, redirect to the scoreboard

