from .levels import levels


def run(code, level):
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]
    victory = False

    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    try:
        exec(code, globals(), d)
        d['move'](robot)
        if robot.coins_collected == data['coins']:
            victory = True
        return {"results": world.get_data(), "success": True, "victory": victory }
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"results": str(e), "success": False, "victory": False }
