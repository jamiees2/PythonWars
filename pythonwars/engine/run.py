from .levels import levels


def run(code, level):
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]

    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    try:
        exec(code, globals(), d)
        d['move'](robot)
        return {"results": world.get_data(), "success": True }
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"results": str(e), "success": False }
