# PythonWars
PythonWars is an online game written in python. In PythonWars you write a robot
in python to solve a variety of tasks. You can compete against other
user-generated robots and race to the top spot on the leaderboard.

# Installation
## Requirements
* `python3`
You will also need to install all of the python modules referenced in
`requirements.txt`
```
pip3 install -r requirements.txt
```

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
