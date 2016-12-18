from .levels import levels, MODE_REGULAR, MODE_INVISIBLE
import subprocess
import sys
import json
import os


def run(code, level):
    """Runs the given user code on the input"""

    # Load the level data
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]
    mode = data.get("mode", MODE_REGULAR)

    victory = False
    g = {}
    try:
        # Load the user's code, use the same empty global variable
        exec(code, g, g)
        g["_robot"] = robot
        # Call the user's code using the same global scope, this allows the user to define multiple functions
        exec("move(_robot)", g, g)

        # If the user's robot collected all the coins, then he won
        if robot.coins_collected == data['coins']:
            victory = True
        moves = robot.moves
        # hide the level if the mode was invisible
        out = world.get_data(hidden=(mode == MODE_INVISIBLE and not victory))
        return {"results": out, "success": True, "victory": victory, "moves": moves}
    except Exception as e:
        # If there was any error, let the user know
        print("Unexpected error:", str(e))
        return {"results": str(e), "success": False, "victory": False}


def run_subprocess(code, level):
    # Spawn a subprocess running runengine in the parent directory
    program = [sys.executable, os.path.join(os.path.dirname(__file__), "..", "runengine.py"), level]
    try:
        response = subprocess.run(program, input=code.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
    except subprocess.TimeoutExpired:
        # Code timed out
        return {"results": "Timeout occured after 2 seconds", "success": False, "victory": False}
    # Get the output
    o = response.stdout.decode('utf-8')
    e = response.stderr.decode('utf-8')
    if e:
        print(repr(e))
        return {"results": "An unknown error occured", "success": False, "victory": False}
    # The last thing that should be printed is JSONOUTPUT followed by the json response of run
    o, js = o.split("JSONOUTPUT", 2)
    print(o)
    js = js.strip()
    return json.loads(js)

