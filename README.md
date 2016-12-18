# PythonWars
PythonWars is an online game written in python. In PythonWars you write a robot
in python to solve a variety of tasks. You can compete against other
user-generated robots and race to the top spot on the leaderboard.

# Description
An online coding game, where the goal is to navigate through a maze and collect all the coins. This is done by programming a robot in python to make him go through the maze.

The score upon completing a level is how many steps the robot needed, the goal is therefore to complete the level in as few moves as possible. Ties are broken by number of characters used in the code. 

## Game modes
`Normal mode`: user sees the maze and needs to write his code to direct the robot the right way.

`Ivisible mode`: user only sees his robot and objects that are close by. This mode is harder since the robot has to check his surroundings to navigate the maze blindly.

## Extra features in the game:
`Portals`, robot goes though a portal and ends up in another portal in the maze. 

`Crates`, robot can push crates around, they can be useful for closing a portal if robot needs to walk across one.

`Plates`, robot can only walk on a plate once, after he passes by it turns into a wall.

# Implementation
When user submits a python code, it is executed on the server. Instructions are generated for the robot, those are then simulated for the user. 

CodeMirror was used for the code submission form and Phaser for the game board. Materialize was used for styling.

# Installation
## Requirements
* `python3`
You will also need to install all of the python modules referenced in
`requirements.txt`
```
pip3 install -r requirements.txt
```

# PyPI packages used
`bcrypt`

`Flask`, `Flask-Migrate`, `Flask-Script` and `Flask-SQLAlchemy`

`voluptuous`

`passlib`

## Database
To set up the database you need to run the following commands
```
python3 pythonwars.py db init
python3 pythonwars.py db migrate
python3 pythonwars.py db upgrade
```

# Usage
To run the python server, execute the following command
```
python3 pythonwars.py runserver
```

# Authors
* Elísa Rún Hermundardóttir
* Hlynur Óskar Guðmundsson
* James Elías Sigurðarson
