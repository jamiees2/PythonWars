from .levels import levels, MODE_REGULAR, MODE_INVISIBLE
import subprocess
import sys
import json
import os


def run(code, level):
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]
    mode = data.get("mode", MODE_REGULAR)
    victory = False

    g = {}
    try:
        exec(code, g, g)
        g["_robot"] = robot
        exec("move(_robot)", g, g)
        if robot.coins_collected == data['coins']:
            victory = True
            moves = robot.moves
        # hide the level if the mode was invisible
        out = world.get_data(hidden=(mode == MODE_INVISIBLE and not victory))
        return {"results": out, "success": True, "victory": victory, "moves": moves}
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"results": str(e), "success": False, "victory": False}


def run_subprocess(code, level):
    program = [sys.executable, os.path.join(os.path.dirname(__file__), "..", "runengine.py"), level]
    try:
        response = subprocess.run(program, input=code.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
    except subprocess.TimeoutExpired:
        return {"results": "Timeout occured after 2 seconds", "success": False, "victory": False}
    o = response.stdout.decode('utf-8')
    e = response.stderr.decode('utf-8')
    if e:
        print(repr(e))
        return {"results": "An unknown error occured", "success": False, "victory": False}
    o, js = o.split("JSONOUTPUT", 2)
    print(o)
    js = js.strip()
    print(js)
    return json.loads(js)

