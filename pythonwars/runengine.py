import sys
import json


def main(args):
    level = args[0]
    code = sys.stdin.read()
    from engine.run import run
    out = run(code, level)
    # Prepare the receiver for the rest of the output
    print("JSONOUTPUT")
    print(json.dumps(out))

if __name__ == '__main__':
    main(sys.argv[1:])
