from .levels import levels, MODE_REGULAR, MODE_INVISIBLE
from .world import WALL


def run(code, level):
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]
    mode = data.get("mode", MODE_REGULAR)
    victory = False

    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    try:
        exec(code, globals(), d)
        d['move'](robot)
        if robot.coins_collected == data['coins']:
            victory = True
        # hide the level if the mode was invisible
        out = world.get_data(hidden=(mode == MODE_INVISIBLE and not victory))
        return {"results": out, "success": True, "victory": victory}
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"results": str(e), "success": False, "victory": False}
